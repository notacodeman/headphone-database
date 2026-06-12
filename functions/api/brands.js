// GET /api/brands — public endpoint powering the brand pages. With no query string
// it returns every manufacturer; with ?id=N it returns one brand plus all of that
// brand's products. This is a read-only companion to /api/catalog used by brand.html.

// Small helper that wraps any payload in a JSON Response with open CORS, so each
// return below stays a one-liner instead of repeating the header boilerplate.
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
      // Single-brand mode: first fetch the manufacturer row itself. parseInt guards
      // against non-numeric input, and a missing brand returns a clean 404.
      const brand = await env.DB.prepare(
        "SELECT * FROM manufacturers WHERE manufacturer_id = ?"
      ).bind(parseInt(id, 10)).first();
      if (!brand) return json({ ok: false, error: "Brand not found" }, 404);

      // Then fetch every product for that brand, ordered chronologically so the
      // brand page can lay them out as a timeline / lineage from oldest to newest.
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

    // List mode (no id): return all manufacturers alphabetically for index/nav use.
    const { results } = await env.DB.prepare(
      "SELECT * FROM manufacturers ORDER BY name ASC"
    ).all();
    return json({ ok: true, brands: results });
  } catch (err) {
    // Surface the error message (not just a generic string) since these are
    // read-only queries with no sensitive data, which makes debugging easier.
    return json({ ok: false, error: String(err && err.message || err) }, 500);
  }
}
