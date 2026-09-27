// /api/admin/suggestions (behind Cloudflare Access)
//   GET                                                  -> every suggestion, newest first
//   POST { id, action: "accept", product_id, changes, note } -> apply changes to the product
//   POST { id, action: "reject", note }
//   POST { id, action: "reopen" }                        -> move a rejected suggestion back to pending
//
// Suggestions are never deleted, so the table doubles as a permanent log.

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });

// Product columns an accepted suggestion is allowed to change.
const APPLICABLE_FIELDS = [
  "driver_size_mm", "impedance_ohms", "sensitivity_db",
  "connector_type", "detachable_cable", "weight_g",
];

export async function onRequestGet({ env }) {
  try {
    const { results } = await env.DB.prepare(
      "SELECT * FROM suggestions ORDER BY created_at DESC, id DESC"
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

    const suggestion = await env.DB.prepare(
      "SELECT id, status FROM suggestions WHERE id = ?"
    ).bind(id).first();
    if (!suggestion) return json({ ok: false, error: "Suggestion not found." }, 404);

    const note = (body.note || "").toString().trim().slice(0, 2000) || null;
    const now = new Date().toISOString();

    switch (body.action) {
      case "accept":
        if (suggestion.status !== "pending") {
          return json({ ok: false, error: `Suggestion is already ${suggestion.status}.` }, 409);
        }
        return accept(env, id, body, note, now);

      case "reject":
        if (suggestion.status !== "pending") {
          return json({ ok: false, error: `Suggestion is already ${suggestion.status}.` }, 409);
        }
        await env.DB.prepare(
          "UPDATE suggestions SET status = 'rejected', resolved_at = ?, admin_note = ? WHERE id = ?"
        ).bind(now, note, id).run();
        return json({ ok: true });

      case "reopen":
        // Accepted suggestions have already changed a product; undo those through
        // the product's history instead.
        if (suggestion.status === "accepted") {
          return json({ ok: false, error: "Accepted suggestions can't be reopened." }, 409);
        }
        await env.DB.prepare(
          `UPDATE suggestions
           SET status = 'pending', resolved_at = NULL, admin_note = NULL,
               product_id = NULL, applied_changes = NULL
           WHERE id = ?`
        ).bind(id).run();
        return json({ ok: true });

      default:
        return json({ ok: false, error: "Unknown action." }, 400);
    }
  } catch (err) {
    return json({ ok: false, error: String(err?.message || err) }, 500);
  }
}

async function accept(env, id, body, note, now) {
  const productId = (body.product_id || "").toString().trim();
  if (!productId) return json({ ok: false, error: "Pick the product this suggestion applies to." }, 400);

  const product = await env.DB.prepare(
    "SELECT * FROM products WHERE product_id = ?"
  ).bind(productId).first();
  if (!product) return json({ ok: false, error: `No product with id ${productId}.` }, 404);

  const requested = body.changes && typeof body.changes === "object" ? body.changes : {};
  const unknown = Object.keys(requested).filter(f => !APPLICABLE_FIELDS.includes(f));
  if (unknown.length) return json({ ok: false, error: `Can't apply: ${unknown.join(", ")}` }, 400);

  // Keep only real changes, so the log shows exactly what moved.
  const applied = {};
  for (const [field, raw] of Object.entries(requested)) {
    const to = (raw ?? "").toString().trim();
    const from = (product[field] ?? "").toString();
    if (to !== from) applied[field] = { from, to };
  }

  const statements = [];
  const fields = Object.keys(applied);
  if (fields.length) {
    statements.push(
      env.DB.prepare(
        "INSERT INTO product_history (product_id, edited_at, snapshot) VALUES (?, ?, ?)"
      ).bind(productId, now, JSON.stringify(product)),
      env.DB.prepare(
        `UPDATE products SET ${fields.map(f => `${f} = ?`).join(", ")}, date_updated = ?
         WHERE product_id = ?`
      ).bind(...fields.map(f => applied[f].to), now.slice(0, 10), productId)
    );
  }
  statements.push(
    env.DB.prepare(
      `UPDATE suggestions
       SET status = 'accepted', product_id = ?, resolved_at = ?, applied_changes = ?, admin_note = ?
       WHERE id = ?`
    ).bind(productId, now, JSON.stringify(applied), note, id)
  );

  // D1 runs a batch as a single transaction: the product, its history and the
  // log entry all change together or not at all.
  await env.DB.batch(statements);
  return json({ ok: true, product_id: productId, applied });
}
