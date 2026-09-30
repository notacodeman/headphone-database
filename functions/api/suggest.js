// POST /api/suggest: stores a community edit from suggest.html as a pending suggestion.
// This route is public, so it relies on a honeypot and length limits instead of auth.

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};
const MAX_FIELD_LENGTH = 2000;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });

export async function onRequestPost({ request, env }) {
  try {
    const form = await request.formData();
    const field = (name) => (form.get(name) || "").toString().trim().slice(0, MAX_FIELD_LENGTH);

    // "_gotcha" is hidden from people, so only bots fill it in. Pretend it worked and store nothing.
    if (field("_gotcha")) return json({ ok: true });

    const headphone = field("headphone");
    const source = field("source");
    if (!headphone || !source) {
      return json({ ok: false, error: "Headphone and source link are required." }, 400);
    }

    await env.DB.prepare(
      `INSERT INTO suggestions
       (headphone, driver_size_mm, impedance_ohms, sensitivity_db,
        connector, detachable, weight_g, notes, source, submitter, status, created_at)
       VALUES (?,?,?,?,?,?,?,?,?,?, 'pending', ?)`
    ).bind(
      headphone,
      field("driver_size_mm"),
      field("impedance_ohms"),
      field("sensitivity_db"),
      field("connector"),
      field("detachable"),
      field("weight_g"),
      field("notes"),
      source,
      field("submitter"),
      new Date().toISOString()
    ).run();

    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: "Could not save suggestion." }, 500);
  }
}

export async function onRequestOptions() {
  return new Response(null, { headers: CORS_HEADERS });
}
