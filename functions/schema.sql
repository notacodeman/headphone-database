-- D1 tables that live only in the database (the catalog tables are created by
-- /api/admin/import). Paste into the Cloudflare dashboard: D1 > database > Console.

CREATE TABLE IF NOT EXISTS suggestions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    headphone       TEXT NOT NULL,
    driver_size_mm  TEXT,
    impedance_ohms  TEXT,
    sensitivity_db  TEXT,
    connector       TEXT,
    detachable      TEXT,
    weight_g        TEXT,
    notes           TEXT,
    source          TEXT NOT NULL,
    submitter       TEXT,
    status          TEXT DEFAULT 'pending',   -- pending | accepted | rejected
    created_at      TEXT,
    -- Filled in when the suggestion is resolved:
    product_id      TEXT,   -- catalog product it was applied to
    resolved_at     TEXT,
    applied_changes TEXT,   -- JSON: { field: { "from": old, "to": new } }
    admin_note      TEXT
);

-- One row per product save, holding the row as it was before that save.
CREATE TABLE IF NOT EXISTS product_history (
    history_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   TEXT NOT NULL,
    edited_at    TEXT NOT NULL,
    snapshot     TEXT NOT NULL
);

-- Migration for databases created before the resolution columns existed.
-- Run each line once; D1 reports "duplicate column" if it has already been applied.
--
-- ALTER TABLE suggestions ADD COLUMN product_id TEXT;
-- ALTER TABLE suggestions ADD COLUMN resolved_at TEXT;
-- ALTER TABLE suggestions ADD COLUMN applied_changes TEXT;
-- ALTER TABLE suggestions ADD COLUMN admin_note TEXT;
