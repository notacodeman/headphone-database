// Helpers shared by every page. Load this before the page's own script.

// Makes text safe to drop into HTML, including inside attribute values.
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[ch]);
}

// "1299" -> "$1,299"
function formatPrice(usd) {
  return "$" + Number(usd).toLocaleString();
}
