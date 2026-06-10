// /api/suggestions  — admin endpoint, protected by Cloudflare Access.
//   GET                -> list all suggestions (newest first)
//   POST {id, action}  -> action "delete" removes a row; "reviewed" marks it reviewed
// env.DB is the bound D1 database.

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export async function onRequestGet({ env }) {
  try {
    const { results } = await env.DB.prepare(
      `SELECT id, headphone, driver_size_mm, impedance_ohms, sensitivity_db,
              connector, detachable, weight_g, notes, source, submitter, status, created_at
       FROM suggestions ORDER BY created_at DESC`
    ).all();
    return json({ ok: true, suggestions: results || [] });
  } catch (err) {
    return json({ ok: false, error: "Could not load suggestions." }, 500);
  }
}

export async function onRequestPost({ request, env }) {
  try {
    const body = await request.json();
    const id = parseInt(body.id, 10);
    if (!id) return json({ ok: false, error: "Missing id." }, 400);

    if (body.action === "delete") {
      await env.DB.prepare(`DELETE FROM suggestions WHERE id = ?`).bind(id).run();
    } else if (body.action === "reviewed") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'reviewed' WHERE id = ?`).bind(id).run();
    } else if (body.action === "pending") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'pending' WHERE id = ?`).bind(id).run();
    } else {
      return json({ ok: false, error: "Unknown action." }, 400);
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: "Action failed." }, 500);
  }
}
