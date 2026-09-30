// GET /api/brands        -> every manufacturer, A to Z (brands.html)
// GET /api/brands?id=N   -> one manufacturer and its products, oldest first (brand.html)

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
  });

export async function onRequestGet({ env, request }) {
  try {
    const idParam = new URL(request.url).searchParams.get("id");

    if (!idParam) {
      const { results } = await env.DB.prepare("SELECT * FROM manufacturers ORDER BY name ASC").all();
      return json({ ok: true, brands: results });
    }

    const brandId = parseInt(idParam, 10);
    const brand = await env.DB.prepare("SELECT * FROM manufacturers WHERE manufacturer_id = ?")
      .bind(brandId).first();
    if (!brand) return json({ ok: false, error: "Brand not found" }, 404);

    // Oldest first, so the brand page can show the line-up as a timeline.
    const { results: products } = await env.DB.prepare(
      `SELECT id, product_id, model_name, full_name, release_year,
              discontinued_year, status, design, fit, driver_type,
              driver_size_mm, impedance_ohms, sensitivity_db,
              wireless, anc, predecessor, successor, notes,
              category, spec_confidence, msrp_usd
       FROM products
       WHERE manufacturer_id = ?
       ORDER BY release_year ASC, model_name ASC`
    ).bind(brandId).all();

    return json({ ok: true, brand, products });
  } catch (err) {
    // Read-only public data, so showing the real error is harmless and helps debugging.
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}
