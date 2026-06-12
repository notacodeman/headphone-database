// GET /api/admin/history?product_id=SONY_WH1000XM5 — admin-only, protected by
// Cloudflare Access along with every other /api/admin/* route. Returns the full
// edit history for one product, newest first, so the admin UI can show a timeline.
// Each stored snapshot is the product's state BEFORE that edit, enabling rollback/diff.

// JSON Response helper. Note there is no CORS header here: admin routes are meant
// to be reached only from the same-origin admin page behind Access, not cross-site.
const json = (o, s = 200) =>
  new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });

export async function onRequestGet({ request, env }) {
  try {
    // product_id is required; without it there is nothing to look up, so reject early.
    const url = new URL(request.url);
    const product_id = (url.searchParams.get("product_id") || "").trim();
    if (!product_id) return json({ ok: false, error: "product_id is required." }, 400);

    // Pull every history row for this product, newest first (history_id is a rising
    // integer, so DESC gives reverse-chronological order without needing a timestamp sort).
    const { results } = await env.DB.prepare(
      `SELECT history_id, edited_at, snapshot
       FROM product_history
       WHERE product_id = ?
       ORDER BY history_id DESC`
    ).bind(product_id).all();

    // Each snapshot is stored as a JSON string; parse it back into an object so the
    // client receives structured data. The "{}" default guards against a null column.
    const history = (results || []).map(row => ({
      history_id: row.history_id,
      edited_at: row.edited_at,
      snapshot: JSON.parse(row.snapshot || "{}")
    }));

    return json({ ok: true, product_id, history });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
