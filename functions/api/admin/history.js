// GET /api/admin/history?product_id=SONY_WH1000XM5
// Every saved edit of one product, newest first. Each snapshot is the row as it was
// *before* that edit, so the admin page can diff consecutive entries.

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });

export async function onRequestGet({ request, env }) {
  try {
    const productId = (new URL(request.url).searchParams.get("product_id") || "").trim();
    if (!productId) return json({ ok: false, error: "product_id is required." }, 400);

    // history_id only ever increases, so sorting by it gives newest first.
    const { results } = await env.DB.prepare(
      `SELECT history_id, edited_at, snapshot
       FROM product_history
       WHERE product_id = ?
       ORDER BY history_id DESC`
    ).bind(productId).all();

    const history = (results || []).map(row => ({
      history_id: row.history_id,
      edited_at: row.edited_at,
      snapshot: JSON.parse(row.snapshot || "{}"),
    }));

    return json({ ok: true, product_id: productId, history });
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}
