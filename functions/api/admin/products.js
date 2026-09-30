// /api/admin/products
//   GET                    -> every product with its brand name
//   GET ?manufacturers=1   -> just the brand list, for the editor's Brand dropdown
//   POST {product}         -> insert or update one product (keyed by product_id)
//   DELETE {product_id}    -> delete one product

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

// Every column a save writes. The upsert is built from this list, so a new editable
// column only needs adding here.
const PRODUCT_COLUMNS = [
  "product_id", "id", "family_id", "manufacturer_id", "model_name", "full_name",
  "release_year", "discontinued_year", "status", "category", "design", "fit", "driver_type",
  "driver_size_mm", "impedance_ohms", "sensitivity_db", "wireless", "anc",
  "predecessor", "successor", "notes", "date_added", "spec_confidence",
  "msrp_usd", "sound_signature", "connector_type", "detachable_cable", "weight_g",
];
const INTEGER_COLUMNS = new Set(["id", "manufacturer_id", "release_year"]);

const today = () => new Date().toISOString().slice(0, 10);

export async function onRequestGet({ request, env }) {
  try {
    if (new URL(request.url).searchParams.get("manufacturers")) {
      const { results } = await env.DB.prepare(
        "SELECT manufacturer_id, name FROM manufacturers ORDER BY name"
      ).all();
      return json({ ok: true, manufacturers: results || [] });
    }
    const { results } = await env.DB.prepare(
      `SELECT p.*, m.name AS _brand
       FROM products p LEFT JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
       ORDER BY p.release_year DESC`
    ).all();
    return json({ ok: true, products: results || [] });
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}

export async function onRequestPost({ request, env }) {
  try {
    const product = await request.json();
    const productId = (product.product_id || "").toString().trim();
    if (!productId) return json({ ok: false, error: "product_id is required." }, 400);
    if (!(product.model_name || "").toString().trim()) {
      return json({ ok: false, error: "model_name is required." }, 400);
    }

    const existing = await env.DB.prepare("SELECT * FROM products WHERE product_id = ?")
      .bind(productId).first();

    if (existing) {
      // Snapshot the row before overwriting it. A failed history write shouldn't block the save.
      try {
        await env.DB.prepare(
          "INSERT INTO product_history (product_id, edited_at, snapshot) VALUES (?, ?, ?)"
        ).bind(productId, new Date().toISOString(), JSON.stringify(existing)).run();
      } catch (_) {}
    } else if (product.id === undefined || product.id === null || product.id === "") {
      // New product: take the next sequential id, the same scheme _generate_data.py uses.
      const { nextId } = await env.DB.prepare(
        "SELECT COALESCE(MAX(id), 0) + 1 AS nextId FROM products"
      ).first();
      product.id = nextId;
    }

    // A column missing from the request (like `id` or `family_id`, which the editor
    // doesn't send) keeps its stored value. A column sent as "" was cleared on purpose.
    const values = PRODUCT_COLUMNS.map(column => {
      let value = product[column];
      if (value === undefined && existing) value = existing[column];
      if (value === undefined || value === null) value = "";
      if (INTEGER_COLUMNS.has(column)) {
        const number = parseInt(value, 10);
        return Number.isFinite(number) ? number : null;
      }
      if (column === "date_added") return value.toString().trim() || today();
      return value.toString();
    });

    // date_updated is always set here, never taken from the client.
    const columns = [...PRODUCT_COLUMNS, "date_updated"];
    const updateList = columns.filter(c => c !== "product_id").map(c => `${c}=excluded.${c}`).join(",");
    await env.DB.prepare(
      `INSERT INTO products (${columns.join(",")}) VALUES (${columns.map(() => "?").join(",")})
       ON CONFLICT(product_id) DO UPDATE SET ${updateList}`
    ).bind(...values, today()).run();

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}

// Deleting skips the history table, so it's permanent. The admin page confirms first.
export async function onRequestDelete({ request, env }) {
  try {
    const { product_id: productId } = await request.json();
    if (!productId) return json({ ok: false, error: "product_id is required." }, 400);
    await env.DB.prepare("DELETE FROM products WHERE product_id = ?").bind(productId).run();
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}
