// GET /api/catalog — public, unauthenticated endpoint. Returns the entire product
// catalog from the D1 database as JSON, which is what the public archive site reads
// on load. D1 is the live source of truth; the CSVs in the repo are only a backup/seed,
// so the front-end prefers this endpoint and falls back to the CSVs only if it fails.

export async function onRequestGet({ env }) {
  // CORS is wide-open because this is public data, and a short cache window lets
  // Cloudflare serve repeat hits without re-querying D1 every single request.
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "public, max-age=60",
  };
  try {
    // Join each product to its manufacturer so the brand name (and founding year)
    // travel with the row; the underscore-prefixed aliases mark fields that are
    // derived from the join rather than stored on the products table itself.
    const { results } = await env.DB.prepare(
      `SELECT p.id, p.product_id, p.manufacturer_id, m.name AS _brand, m.founded_year AS _founded,
              p.model_name, p.full_name, p.release_year, p.discontinued_year,
              p.status, p.category, p.design, p.fit, p.driver_type,
              p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
              p.wireless, p.anc, p.predecessor, p.successor, p.notes, p.spec_confidence,
              p.msrp_usd, p.sound_signature, p.connector_type, p.detachable_cable, p.weight_g
       FROM products p
       LEFT JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
       ORDER BY p.release_year DESC`
    ).all();
    return new Response(JSON.stringify({ ok: true, products: results || [] }), { headers });
  } catch (err) {
    // Any DB failure returns a clean 500 with a generic message rather than leaking
    // internals; the front-end treats this as a signal to fall back to the CSVs.
    return new Response(JSON.stringify({ ok: false, error: "catalog read failed" }), { status: 500, headers });
  }
}
