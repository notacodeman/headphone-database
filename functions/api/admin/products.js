// /api/admin/products — protected by Cloudflare Access.
//   GET                       -> list all products (with brand name)
//   POST {product...}         -> insert or update one product (upsert by product_id)
//   DELETE {product_id}       -> remove a product
// Also serves the manufacturers list via ?manufacturers=1 for the editor's brand dropdown.

// JSON Response helper (same-origin admin use, so no CORS header).
const json = (o, s = 200) =>
  new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });

// The full set of columns the editor can write, in a fixed order. The upsert below
// is built dynamically from this list, so adding a new editable column is a one-line
// change here rather than edits scattered across the INSERT and UPDATE clauses.
const FIELDS = [
  "product_id", "id", "family_id", "manufacturer_id", "model_name", "full_name",
  "release_year", "discontinued_year", "status", "category", "design", "fit", "driver_type",
  "driver_size_mm", "impedance_ohms", "sensitivity_db", "wireless", "anc",
  "predecessor", "successor", "notes", "date_added", "spec_confidence",
  "msrp_usd", "sound_signature", "connector_type", "detachable_cable", "weight_g",
];

export async function onRequestGet({ request, env }) {
  try {
    // Dual-purpose GET. With ?manufacturers=1 it returns just the brand list, which
    // the editor uses to populate its brand dropdown without loading every product.
    const url = new URL(request.url);
    if (url.searchParams.get("manufacturers")) {
      const { results } = await env.DB.prepare(
        "SELECT manufacturer_id, name FROM manufacturers ORDER BY name"
      ).all();
      return json({ ok: true, manufacturers: results || [] });
    }
    // Otherwise return every product joined to its brand name, newest first — the
    // dataset that fills the admin table.
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
    // POST upserts one product keyed by product_id. Both product_id and model_name
    // are mandatory; reject early so we never write a half-identified row.
    const p = await request.json();
    const id = (p.product_id || "").toString().trim();
    if (!id) return json({ ok: false, error: "product_id is required." }, 400);
    if (!(p.model_name || "").toString().trim())
      return json({ ok: false, error: "model_name is required." }, 400);

    // Look up the existing row (if any) BEFORE overwriting it, both to snapshot it for
    // version history and to recover its `id`. The editor form never exposes `id` as a
    // field (it's assigned, not user-edited), so the client never sends it — without this
    // lookup every save would coerce the missing value to null and wipe the row's id.
    const existing = await env.DB.prepare(
      "SELECT * FROM products WHERE product_id = ?"
    ).bind(id).first();
    if (existing) {
      try {
        const editedAt = new Date().toISOString();
        await env.DB.prepare(
          "INSERT INTO product_history (product_id, edited_at, snapshot) VALUES (?, ?, ?)"
        ).bind(id, editedAt, JSON.stringify(existing)).run();
      } catch (_) { /* history write failure should never block the actual save */ }
    }

    // Brand-new product (no existing row) with no id sent — assign the next free
    // sequential id, matching the identity scheme _generate_data.py uses. Updates to an
    // existing product fall back to its current id via the `existing` lookup below.
    if (!existing && (p.id === undefined || p.id === null || p.id === "")) {
      const next = await env.DB.prepare(
        "SELECT COALESCE(MAX(id), 0) + 1 AS next FROM products"
      ).first();
      p.id = next.next;
    }

    // Coerce each field to a DB-safe value. Numeric columns parse to integers (or
    // null if unparseable), date_added defaults to today when blank, and everything
    // else is stored as a trimmed string — keeping types consistent with the schema.
    // A field that's entirely absent from the request (e.g. `family_id`, which FIELDS
    // tracks but the editor UI doesn't yet expose) falls back to the existing row's
    // value on update rather than being coerced to blank — same reasoning as `id` above,
    // generalised so adding a server-side field doesn't silently erase it until the
    // editor catches up. A field the client explicitly sent as "" is left alone: that's
    // the user clearing it on purpose.
    const vals = FIELDS.map(f => {
      let v = p[f];
      if (v === undefined && existing) v = existing[f];
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

    // Build the upsert dynamically from FIELDS plus a server-set date_updated.
    // ON CONFLICT(product_id) turns this into an insert-or-update: a new product_id
    // inserts, an existing one updates every column from the submitted values.
    // date_updated is always server-set (never trusted from the client).
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
    // Permanently remove one product by id. Note this does not snapshot to history,
    // so deletion is final — the admin UI is expected to confirm before calling this.
    const { product_id } = await request.json();
    if (!product_id) return json({ ok: false, error: "product_id required." }, 400);
    await env.DB.prepare("DELETE FROM products WHERE product_id = ?").bind(product_id).run();
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
