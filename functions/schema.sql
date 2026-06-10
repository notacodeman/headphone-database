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
