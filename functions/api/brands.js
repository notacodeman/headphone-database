const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
  });

export async function onRequestGet({ env, request }) {
  try {
    const url = new URL(request.url);
    const id = url.searchParams.get("id");

    if (id) {
      // Single brand with product stats
      const brand = await env.DB.prepare(
        "SELECT * FROM manufacturers WHERE manufacturer_id = ?"
      ).bind(parseInt(id, 10)).first();
      if (!brand) return json({ ok: false, error: "Brand not found" }, 404);

      const { results: products } = await env.DB.prepare(
        `SELECT p.id, p.product_id, p.model_name, p.full_name, p.release_year,
                p.discontinued_year, p.status, p.design, p.fit, p.driver_type,
                p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
                p.wireless, p.anc, p.predecessor, p.successor, p.notes,
                p.category, p.spec_confidence
         FROM products p
         WHERE p.manufacturer_id = ?
         ORDER BY p.release_year ASC, p.model_name ASC`
      ).bind(parseInt(id, 10)).all();

      return json({ ok: true, brand, products });
    }

    // All brands
    const { results } = await env.DB.prepare(
      "SELECT * FROM manufacturers ORDER BY name ASC"
    ).all();
    return json({ ok: true, brands: results });
  } catch (err) {
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
