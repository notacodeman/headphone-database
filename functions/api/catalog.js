// GET /api/catalog: the whole catalog for the public archive page.
// D1 is the live source of truth. If this fails, index.html falls back to the CSVs on GitHub.

const headers = {
  "Content-Type": "application/json",
  "Access-Control-Allow-Origin": "*",
  // A short cache lets Cloudflare answer repeat visits without hitting D1 every time.
  "Cache-Control": "public, max-age=60",
};

// Columns prefixed with _ come from the manufacturers join, not the products table.
const CATALOG_QUERY = `
  SELECT p.id, p.product_id, p.manufacturer_id, m.name AS _brand, m.founded_year AS _founded,
         p.model_name, p.full_name, p.release_year, p.discontinued_year,
         p.status, p.category, p.design, p.fit, p.driver_type,
         p.driver_size_mm, p.impedance_ohms, p.sensitivity_db,
         p.wireless, p.anc, p.predecessor, p.successor, p.notes, p.spec_confidence,
         p.msrp_usd, p.sound_signature, p.connector_type, p.detachable_cable, p.weight_g
  FROM products p
  LEFT JOIN manufacturers m ON m.manufacturer_id = p.manufacturer_id
  ORDER BY p.release_year DESC`;

export async function onRequestGet({ env }) {
  try {
    const { results } = await env.DB.prepare(CATALOG_QUERY).all();
    return new Response(JSON.stringify({ ok: true, products: results || [] }), { headers });
  } catch (err) {
    return new Response(JSON.stringify({ ok: false, error: "Catalog read failed." }), { status: 500, headers });
  }
}
