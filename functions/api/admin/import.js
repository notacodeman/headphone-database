// POST /api/admin/import — protected by Cloudflare Access.
// Fetches the CSVs from GitHub, (re)creates the catalog tables in D1, and loads them.
// Safe to re-run: it wipes and reloads the products & manufacturers tables.
// NOTE: re-running OVERWRITES live edits with whatever is in the CSVs, so only
// use this for the initial seed or a deliberate reset from a known-good CSV.

const RAW_BASE = "https://raw.githubusercontent.com/notacodeman/headphone-database/main/database";

function parseCSV(text) {
  const rows = []; let row = [], field = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i+1] === '"') { field += '"'; i++; } else q = false; } else field += c; }
    else {
      if (c === '"') q = true;
      else if (c === ',') { row.push(field); field = ""; }
      else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ""; }
      else if (c === '\r') {}
      else field += c;
    }
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const header = rows.shift();
  return rows.filter(r => r.length > 1).map(r => {
    const o = {}; header.forEach((h, i) => o[h.trim()] = (r[i] || "").trim()); return o;
  });
}

const json = (o, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });

export async function onRequestPost({ env }) {
  try {
    const [pTxt, mTxt] = await Promise.all([
      fetch(RAW_BASE + "/products.csv").then(r => r.text()),
      fetch(RAW_BASE + "/manufacturers.csv").then(r => r.text()),
    ]);
    const products = parseCSV(pTxt);
    const manufacturers = parseCSV(mTxt);
    if (!products.length || !manufacturers.length) return json({ ok: false, error: "CSV fetch empty" }, 500);

    // Create tables (id-less mirror of the CSV columns; everything TEXT for simplicity).
    await env.DB.exec(
      "CREATE TABLE IF NOT EXISTS manufacturers (manufacturer_id INTEGER PRIMARY KEY, name TEXT, country TEXT, website TEXT, status TEXT);"
    );
    await env.DB.exec(
      "CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, family_id TEXT, manufacturer_id INTEGER, model_name TEXT, full_name TEXT, release_year INTEGER, discontinued_year TEXT, status TEXT, category TEXT, design TEXT, driver_type TEXT, driver_size_mm TEXT, impedance_ohms TEXT, sensitivity_db TEXT, wireless TEXT, anc TEXT, predecessor TEXT, successor TEXT, notes TEXT, date_added TEXT);"
    );

    // Wipe and reload.
    await env.DB.exec("DELETE FROM products;");
    await env.DB.exec("DELETE FROM manufacturers;");

    // Insert manufacturers.
    const mStmt = env.DB.prepare(
      "INSERT INTO manufacturers (manufacturer_id,name,country,website,status) VALUES (?,?,?,?,?)"
    );
    const mBatch = manufacturers.map(m =>
      mStmt.bind(parseInt(m.manufacturer_id, 10) || null, m.name, m.country, m.website, m.status));
    for (let i = 0; i < mBatch.length; i += 40) await env.DB.batch(mBatch.slice(i, i + 40));

    // Insert products (chunked to stay within batch limits).
    const pStmt = env.DB.prepare(
      `INSERT INTO products
       (product_id,family_id,manufacturer_id,model_name,full_name,release_year,discontinued_year,
        status,category,design,driver_type,driver_size_mm,impedance_ohms,sensitivity_db,
        wireless,anc,predecessor,successor,notes,date_added)
       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`
    );
    const pBatch = products.map(p => pStmt.bind(
      p.product_id, p.family_id, parseInt(p.manufacturer_id, 10) || null, p.model_name, p.full_name,
      parseInt(p.release_year, 10) || null, p.discontinued_year, p.status, p.category, p.design,
      p.driver_type, p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
      p.wireless, p.anc, p.predecessor, p.successor, p.notes, p.date_added || ""));
    for (let i = 0; i < pBatch.length; i += 40) await env.DB.batch(pBatch.slice(i, i + 40));

    return json({ ok: true, manufacturers: manufacturers.length, products: products.length });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
