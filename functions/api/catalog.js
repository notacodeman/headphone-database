// GET /api/catalog — public. Returns the full catalog from D1 as JSON,
// with each product's brand name joined in. The site reads this instead of CSVs.

export async function onRequestGet({ env }) {
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "public, max-age=60",
  };
  try {
    const { results } = await env.DB.prepare(
      `SELECT p.id, p.product_id, p.manufacturer_id, m.name AS _brand,
              p.model_name, p.full_name, p.release_year, p.discontinued_year,
              p.status, p.category, p.design, p.fit, p.driver_type,
              p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
              p.wireless, p.anc, p.predecessor, p.successor, p.notes, p.date_added
       FROM products p
       LEFT JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
       ORDER BY p.release_year DESC`
    ).all();
    return new Response(JSON.stringify({ ok: true, products: results || [] }), { headers });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: "catalog read failed" }), { status: 500, headers });
  }
}
