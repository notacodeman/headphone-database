// GET /api/admin/history?product_id=SONY_WH1000XM5
// Returns the full edit history for one product, newest first.
// Each row is the state of the product BEFORE that edit was made.
// Protected by Cloudflare Access (same as all /api/admin/* routes).

const json = (o, s = 200) =>
  new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json" } });

export async function onRequestGet({ request, env }) {
  try {
    const url = new URL(request.url);
    const product_id = (url.searchParams.get("product_id") || "").trim();
    if (!product_id) return json({ ok: false, error: "product_id is required." }, 400);

    const { results } = await env.DB.prepare(
      `SELECT history_id, edited_at, snapshot
       FROM product_history
       WHERE product_id = ?
       ORDER BY history_id DESC`
    ).bind(product_id).all();

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
