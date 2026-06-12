// POST /api/suggest — public endpoint that receives a community edit suggestion from
// the suggest.html form and stores it in D1 with a "pending" status for later review.
// Unlike the admin routes this is open to anyone, so it leans on a honeypot and strict
// input limits rather than authentication. The bound D1 database is env.DB (binding "DB").

export async function onRequestPost({ request, env }) {
  // Open CORS so the form can post from the site; JSON content type for the reply.
  const cors = {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  };

  try {
    const form = await request.formData();

    // Spam honeypot: "_gotcha" is a hidden field humans never see or fill. If it has
    // any value, a bot filled it, so we silently pretend success and store nothing.
    if ((form.get("_gotcha") || "").trim() !== "") {
      return new Response(JSON.stringify({ ok: true }), { headers: cors });
    }

    // Read-and-sanitise helper: coerces to string, trims, and hard-caps length at
    // 2000 chars so a malicious payload can't bloat the row or the database.
    const val = (k) => (form.get(k) || "").toString().trim().slice(0, 2000);

    // Headphone name and a source link are the minimum required for a useful
    // suggestion; without either, reject with a 400 before touching the database.
    const headphone = val("headphone");
    const source = val("source");
    if (!headphone || !source) {
      return new Response(
        JSON.stringify({ ok: false, error: "Headphone and source link are required." }),
        { status: 400, headers: cors }
      );
    }

    // Parameterised INSERT (never string-built) so user input can't inject SQL.
    // status is hard-coded to 'pending' and created_at is server-set, so neither can
    // be spoofed by the submitter.
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
    // Generic failure message — the submitter doesn't need (and shouldn't see) DB internals.
    return new Response(
      JSON.stringify({ ok: false, error: "Could not save suggestion." }),
      { status: 500, headers: cors }
    );
  }
}

// CORS preflight handler. Browsers send an OPTIONS request before a cross-origin POST;
// this answers it with the allowed method and headers so the real POST can proceed.
export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
