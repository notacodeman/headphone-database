// POST /api/admin/import: wipes the products and manufacturers tables and reloads them
// from the CSVs on GitHub. This OVERWRITES every live edit, so it's only for the first
// seed or a deliberate reset to a known-good CSV.

const CSV_BASE_URL = "https://raw.githubusercontent.com/notacodeman/headphone-database/main/database";
// D1 limits how many statements one batch() call can hold.
const BATCH_SIZE = 40;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

// Handles quoted fields (commas and newlines inside quotes) and "" escapes.
// Returns one object per row, keyed by the header names.
function parseCsv(text) {
  const rows = [];
  let row = [], cell = "", inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (inQuotes) {
      if (char !== '"') cell += char;
      else if (text[i + 1] === '"') { cell += '"'; i++; }
      else inQuotes = false;
    } else if (char === '"') inQuotes = true;
    else if (char === ",") { row.push(cell); cell = ""; }
    else if (char === "\n") { row.push(cell); rows.push(row); row = []; cell = ""; }
    else if (char !== "\r") cell += char;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }

  const header = rows.shift().map(name => name.trim());
  return rows
    .filter(cells => cells.length > 1) // skip blank lines
    .map(cells => Object.fromEntries(header.map((name, i) => [name, (cells[i] || "").trim()])));
}

const toInt = value => parseInt(value, 10) || null;

async function runInBatches(db, statements) {
  for (let i = 0; i < statements.length; i += BATCH_SIZE) {
    await db.batch(statements.slice(i, i + BATCH_SIZE));
  }
}

export async function onRequestPost({ env }) {
  try {
    const [productsCsv, manufacturersCsv] = await Promise.all([
      fetch(CSV_BASE_URL + "/products.csv").then(r => r.text()),
      fetch(CSV_BASE_URL + "/manufacturers.csv").then(r => r.text()),
    ]);
    const products = parseCsv(productsCsv);
    const manufacturers = parseCsv(manufacturersCsv);
    // An empty file means the fetch went wrong. Stop before wiping anything.
    if (!products.length || !manufacturers.length) {
      return json({ ok: false, error: "A CSV came back empty from GitHub." }, 500);
    }

    await env.DB.exec(
      "CREATE TABLE IF NOT EXISTS manufacturers (manufacturer_id INTEGER PRIMARY KEY, name TEXT, country TEXT, website TEXT, status TEXT, founded_year INTEGER, description TEXT);"
    );
    await env.DB.exec(
      "CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, id INTEGER UNIQUE, family_id TEXT, manufacturer_id INTEGER, model_name TEXT, full_name TEXT, release_year INTEGER, discontinued_year TEXT, status TEXT, category TEXT, design TEXT, driver_type TEXT, driver_size_mm TEXT, impedance_ohms TEXT, sensitivity_db TEXT, wireless TEXT, anc TEXT, predecessor TEXT, successor TEXT, notes TEXT, date_added TEXT, fit TEXT DEFAULT 'Over-Ear', date_updated TEXT, spec_confidence TEXT DEFAULT 'Estimated', msrp_usd TEXT, sound_signature TEXT, connector_type TEXT, detachable_cable TEXT, weight_g TEXT);"
    );
    await env.DB.exec("DELETE FROM products;");
    await env.DB.exec("DELETE FROM manufacturers;");

    const insertManufacturer = env.DB.prepare(
      "INSERT INTO manufacturers (manufacturer_id,name,country,website,status,founded_year,description) VALUES (?,?,?,?,?,?,?)"
    );
    await runInBatches(env.DB, manufacturers.map(m => insertManufacturer.bind(
      toInt(m.manufacturer_id), m.name, m.country, m.website, m.status,
      toInt(m.founded_year), m.description || null
    )));

    const today = new Date().toISOString().slice(0, 10);
    const insertProduct = env.DB.prepare(
      `INSERT INTO products
       (product_id,id,family_id,manufacturer_id,model_name,full_name,release_year,discontinued_year,
        status,category,design,driver_type,driver_size_mm,impedance_ohms,sensitivity_db,
        wireless,anc,predecessor,successor,notes,date_added,fit,date_updated,spec_confidence,
        msrp_usd,sound_signature,connector_type,detachable_cable,weight_g)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    );
    await runInBatches(env.DB, products.map(p => insertProduct.bind(
      p.product_id, toInt(p.id), p.family_id,
      toInt(p.manufacturer_id), p.model_name, p.full_name,
      toInt(p.release_year), p.discontinued_year, p.status, p.category, p.design,
      p.driver_type, p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
      p.wireless, p.anc, p.predecessor, p.successor, p.notes,
      p.date_added || today,
      p.fit || "Over-Ear", today, p.spec_confidence || "Estimated",
      p.msrp_usd, p.sound_signature, p.connector_type, p.detachable_cable, p.weight_g
    )));

    return json({ ok: true, manufacturers: manufacturers.length, products: products.length });
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}
