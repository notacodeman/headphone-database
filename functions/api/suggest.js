// POST /api/suggest  — receives a suggestion from the public form, stores it in D1.
// Bound D1 database is available as env.DB (binding name "DB").

export async function onRequestPost({ request, env }) {
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };

  try {
    const form = await request.formData();

    // Honeypot: bots fill hidden field; real users leave it empty.
    if ((form.get("_gotcha") || "").trim() !== "") {
      return new Response(JSON.stringify({ ok: true }), { headers: cors });
    }

    const val = (k) => (form.get(k) || "").toString().trim().slice(0, 2000);

    const headphone = val("headphone");
    const source = val("source");
    if (!headphone || !source) {
      return new Response(
        JSON.stringify({ ok: false, error: "Headphone and source link are required." }),
        { status: 400, headers: cors }
      );
    }

    await env.DB.prepare(
      `INSERT INTO suggestions
       (headphone, driver_size_mm, impedance_ohms, sensitivity_db,
        connector, detachable, weight_g, notes, source, submitter, status, created_at)
       VALUES (?,?,?,?,?,?,?,?,?,?, 'pending', ?)`
    ).bind(
      headphone,
      val("driver_size_mm"),
      val("impedance_ohms"),
      val("sensitivity_db"),
      val("connector"),
      val("detachable"),
      val("weight_g"),
      val("notes"),
      source,
      val("submitter"),
      new Date().toISOString()
    ).run();

    return new Response(JSON.stringify({ ok: true }), { headers: cors });
  } catch (err) {
    return new Response(
      JSON.stringify({ ok: false, error: "Could not save suggestion." }),
      { status: 500, headers: cors }
    );
  }
}

// Allow the browser's preflight check.
export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
