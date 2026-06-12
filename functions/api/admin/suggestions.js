// /api/admin/suggestions — admin-only, protected by Cloudflare Access. Manages the
// queue of community edit suggestions submitted through the public suggest form.
//   GET                -> list every suggestion, newest first, for the review UI
//   POST {id, action}  -> change one suggestion's state (delete / reviewed / pending /
//                         accept / reject); env.DB is the bound D1 database.

// JSON helper; same-origin admin use only, so no CORS header is set.
const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export async function onRequestGet({ env }) {
  try {
    // Return the whole queue ordered by submission time (newest first) so the
    // reviewer sees the most recent suggestions at the top of the list.
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
    // Every action targets one suggestion by numeric id; reject anything missing it.
    const body = await request.json();
    const id = parseInt(body.id, 10);
    if (!id) return json({ ok: false, error: "Missing id." }, 400);

    // Dispatch on the action string. "delete" removes the row entirely; the rest are
    // status transitions that keep the row but move it through the review workflow.
    // An unrecognised action is rejected rather than silently ignored.
    if (body.action === "delete") {
      await env.DB.prepare(`DELETE FROM suggestions WHERE id = ?`).bind(id).run();
    } else if (body.action === "reviewed") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'reviewed' WHERE id = ?`).bind(id).run();
    } else if (body.action === "pending") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'pending' WHERE id = ?`).bind(id).run();
    } else if (body.action === "accept") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'accepted' WHERE id = ?`).bind(id).run();
    } else if (body.action === "reject") {
      await env.DB.prepare(`UPDATE suggestions SET status = 'rejected' WHERE id = ?`).bind(id).run();
    } else {
      return json({ ok: false, error: "Unknown action." }, 400);
    }
    return json({ ok: true });
  } catch (err) {
    return json({ ok: false, error: "Action failed." }, 500);
  }
}
