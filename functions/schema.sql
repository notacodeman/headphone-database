-- Run once against your D1 database to create the suggestions table.
-- (Cloudflare dashboard: D1 > your database > Console, paste and run.)

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
    status          TEXT DEFAULT 'pending',
    created_at      TEXT
);

-- Version history: one row per save, storing the state BEFORE the edit.
CREATE TABLE IF NOT EXISTS product_history (
    history_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   TEXT NOT NULL,
    edited_at    TEXT NOT NULL,
    snapshot     TEXT NOT NULL  -- full JSON of the row as it was before this edit
);
