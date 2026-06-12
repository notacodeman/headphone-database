// /api/admin/products — protected by Cloudflare Access.
//   GET                       -> list all products (with brand name)
//   POST {product...}         -> insert or update one product (upsert by product_id)
//   DELETE {product_id}       -> remove a product
// Also serves the manufacturers list via ?manufacturers=1 for the editor's brand dropdown.

const json = (o, s = 200) =>
  new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });

const FIELDS = [
  "product_id", "id", "family_id", "manufacturer_id", "model_name", "full_name",
  "release_year", "discontinued_year", "status", "category", "design", "fit", "driver_type",
  "driver_size_mm", "impedance_ohms", "sensitivity_db", "wireless", "anc",
  "predecessor", "successor", "notes", "date_added", "spec_confidence",
  "msrp_usd", "sound_signature", "connector_type", "detachable_cable", "weight_g",
];

export async function onRequestGet({ request, env }) {
  try {
    const url = new URL(request.url);
    if (url.searchParams.get("manufacturers")) {
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
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}

export async function onRequestPost({ request, env }) {
  try {
    const p = await request.json();
    const id = (p.product_id || "").toString().trim();
    if (!id) return json({ ok: false, error: "product_id is required." }, 400);
    if (!(p.model_name || "").toString().trim())
      return json({ ok: false, error: "model_name is required." }, 400);

    // Snapshot existing row BEFORE overwriting it (for version history).
    // Only fires on updates (not new inserts) — no row means nothing to snapshot.
    try {
      const existing = await env.DB.prepare(
        "SELECT * FROM products WHERE product_id = ?"
      ).bind(id).first();
      if (existing) {
        const editedAt = new Date().toISOString();
        await env.DB.prepare(
          "INSERT INTO product_history (product_id, edited_at, snapshot) VALUES (?, ?, ?)"
        ).bind(id, editedAt, JSON.stringify(existing)).run();
      }
    } catch (_) { /* history write failure should never block the actual save */ }

    const vals = FIELDS.map(f => {
      let v = p[f];
      if (v === undefined || v === null) v = "";
      if (f === "id" || f === "manufacturer_id" || f === "release_year") {
        const n = parseInt(v, 10);
        return Number.isFinite(n) ? n : null;
      }
      if (f === "date_added") {
        const s = v.toString().trim();
        return s || new Date().toISOString().slice(0, 10);
      }
      return v.toString();
    });

    const placeholders = FIELDS.map(() => "?").join(",") + ",?";
    const allFields = [...FIELDS, "date_updated"];
    const updates = allFields.filter(f => f !== "product_id")
      .map(f => `${f}=excluded.${f}`).join(",");
    const today = new Date().toISOString().slice(0, 10);

    await env.DB.prepare(
      `INSERT INTO products (${allFields.join(",")}) VALUES (${placeholders})
       ON CONFLICT(product_id) DO UPDATE SET ${updates}`
    ).bind(...vals, today).run();

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}

export async function onRequestDelete({ request, env }) {
  try {
    const { product_id } = await request.json();
    if (!product_id) return json({ ok: false, error: "product_id required." }, 400);
    await env.DB.prepare("DELETE FROM products WHERE product_id = ?").bind(product_id).run();
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
