#!/usr/bin/env python3
"""
build_db.py — Convert headphone database CSVs → headphones.db (SQLite)

Usage:
    python scripts/build_db.py
    python scripts/build_db.py --csv-dir database --db database/headphones.db --verbose
"""

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

# Make output UTF-8 safe on Windows consoles (prevents UnicodeEncodeError
# on box-drawing/checkmark characters).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS manufacturers (
    manufacturer_id  INTEGER PRIMARY KEY,
    name             TEXT    NOT NULL UNIQUE,
    country          TEXT,
    website          TEXT,
    status           TEXT    CHECK(status IN ('Active','Legacy','Defunct'))
);

CREATE TABLE IF NOT EXISTS families (
    family_id        INTEGER PRIMARY KEY,
    manufacturer_id  INTEGER NOT NULL REFERENCES manufacturers(manufacturer_id),
    family_name      TEXT    NOT NULL,
    family_type      TEXT
);

CREATE TABLE IF NOT EXISTS products (
    product_id          TEXT    PRIMARY KEY,
    id                  INTEGER UNIQUE,
    family_id           INTEGER REFERENCES families(family_id),
    manufacturer_id     INTEGER REFERENCES manufacturers(manufacturer_id),
    model_name          TEXT    NOT NULL,
    full_name           TEXT,
    release_year        INTEGER,
    discontinued_year   INTEGER,
    status              TEXT,
    category            TEXT,
    design              TEXT,
    driver_type         TEXT,
    driver_size_mm      TEXT,
    impedance_ohms      TEXT,
    sensitivity_db      TEXT,
    wireless            TEXT    CHECK(wireless IN ('Yes','No')),
    anc                 TEXT    CHECK(anc IN ('Yes','No')),
    predecessor         TEXT    REFERENCES products(product_id),
    successor           TEXT    REFERENCES products(product_id),
    notes               TEXT,
    date_added          TEXT,
    fit                 TEXT    DEFAULT 'Over-Ear'
);

CREATE TABLE IF NOT EXISTS lineage (
    lineage_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    predecessor_product_id  TEXT    REFERENCES products(product_id),
    successor_product_id    TEXT    REFERENCES products(product_id),
    UNIQUE(predecessor_product_id, successor_product_id)
);

CREATE TABLE IF NOT EXISTS sources (
    source_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   TEXT    REFERENCES products(product_id),
    source_type  TEXT,
    title        TEXT,
    url          TEXT
);
"""

INDEXES = """
CREATE INDEX IF NOT EXISTS idx_products_manufacturer  ON products(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_products_family        ON products(family_id);
CREATE INDEX IF NOT EXISTS idx_products_release_year  ON products(release_year);
CREATE INDEX IF NOT EXISTS idx_products_status        ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_design        ON products(design);
CREATE INDEX IF NOT EXISTS idx_products_driver_type   ON products(driver_type);
CREATE INDEX IF NOT EXISTS idx_products_wireless      ON products(wireless);
CREATE INDEX IF NOT EXISTS idx_products_anc           ON products(anc);
CREATE INDEX IF NOT EXISTS idx_sources_product        ON sources(product_id);
CREATE INDEX IF NOT EXISTS idx_lineage_predecessor     ON lineage(predecessor_product_id);
CREATE INDEX IF NOT EXISTS idx_lineage_successor       ON lineage(successor_product_id);
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        print(f"  [WARN] {path} not found — skipping.", file=sys.stderr)
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def coerce_int(val):
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def coerce_str(val):
    if val is None:
        return None
    val = val.strip()
    return val if val else None


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_manufacturers(conn, rows, verbose):
    cur = conn.cursor()
    n = 0
    for r in rows:
        cur.execute("""
            INSERT INTO manufacturers(manufacturer_id, name, country, website, status)
            VALUES (?,?,?,?,?)
            ON CONFLICT(manufacturer_id) DO UPDATE SET
                name=excluded.name,
                country=excluded.country,
                website=excluded.website,
                status=excluded.status
        """, (
            coerce_int(r.get("manufacturer_id")),
            coerce_str(r.get("name")),
            coerce_str(r.get("country")),
            coerce_str(r.get("website")),
            coerce_str(r.get("status")),
        ))
        n += 1
    if verbose:
        print(f"  manufacturers: {n} rows upserted")


def load_families(conn, rows, verbose):
    cur = conn.cursor()
    n = 0
    for r in rows:
        cur.execute("""
            INSERT INTO families(family_id, manufacturer_id, family_name, family_type)
            VALUES (?,?,?,?)
            ON CONFLICT(family_id) DO UPDATE SET
                manufacturer_id=excluded.manufacturer_id,
                family_name=excluded.family_name,
                family_type=excluded.family_type
        """, (
            coerce_int(r.get("family_id")),
            coerce_int(r.get("manufacturer_id")),
            coerce_str(r.get("family_name")),
            coerce_str(r.get("family_type")),
        ))
        n += 1
    if verbose:
        print(f"  families: {n} rows upserted")


def load_products(conn, rows, verbose):
    cur = conn.cursor()
    n = 0
    for r in rows:
        cur.execute("""
            INSERT INTO products(
                product_id, id, family_id, manufacturer_id,
                model_name, full_name, release_year, discontinued_year,
                status, category, design, driver_type,
                driver_size_mm, impedance_ohms, sensitivity_db,
                wireless, anc, predecessor, successor, notes, date_added, fit
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(product_id) DO UPDATE SET
                id=excluded.id, family_id=excluded.family_id,
                manufacturer_id=excluded.manufacturer_id,
                model_name=excluded.model_name, full_name=excluded.full_name,
                release_year=excluded.release_year, discontinued_year=excluded.discontinued_year,
                status=excluded.status, category=excluded.category,
                design=excluded.design, driver_type=excluded.driver_type,
                driver_size_mm=excluded.driver_size_mm, impedance_ohms=excluded.impedance_ohms,
                sensitivity_db=excluded.sensitivity_db, wireless=excluded.wireless,
                anc=excluded.anc, predecessor=excluded.predecessor,
                successor=excluded.successor, notes=excluded.notes,
                date_added=excluded.date_added, fit=excluded.fit
        """, (
            coerce_str(r.get("product_id")), coerce_int(r.get("id")),
            coerce_int(r.get("family_id")), coerce_int(r.get("manufacturer_id")),
            coerce_str(r.get("model_name")), coerce_str(r.get("full_name")),
            coerce_int(r.get("release_year")), coerce_int(r.get("discontinued_year")),
            coerce_str(r.get("status")), coerce_str(r.get("category")),
            coerce_str(r.get("design")), coerce_str(r.get("driver_type")),
            coerce_str(r.get("driver_size_mm")), coerce_str(r.get("impedance_ohms")),
            coerce_str(r.get("sensitivity_db")), coerce_str(r.get("wireless")),
            coerce_str(r.get("anc")), coerce_str(r.get("predecessor")),
            coerce_str(r.get("successor")), coerce_str(r.get("notes")),
            coerce_str(r.get("date_added")), coerce_str(r.get("fit") or "Over-Ear"),
        ))
        n += 1
    if verbose:
        print(f"  products: {n} rows upserted")


def load_lineage(conn, rows, verbose):
    cur = conn.cursor()
    n = 0
    for r in rows:
        cur.execute("""
            INSERT OR IGNORE INTO lineage(predecessor_product_id, successor_product_id)
            VALUES (?,?)
        """, (
            coerce_str(r.get("predecessor_product_id")),
            coerce_str(r.get("successor_product_id")),
        ))
        n += 1
    if verbose:
        print(f"  lineage: {n} rows upserted")


def load_sources(conn, rows, verbose):
    cur = conn.cursor()
    n = 0
    for r in rows:
        source_id = coerce_int(r.get("source_id"))
        if source_id:
            cur.execute("""
                INSERT INTO sources(source_id, product_id, source_type, title, url)
                VALUES (?,?,?,?,?)
                ON CONFLICT(source_id) DO UPDATE SET
                    product_id=excluded.product_id,
                    source_type=excluded.source_type,
                    title=excluded.title,
                    url=excluded.url
            """, (
                source_id,
                coerce_str(r.get("product_id")),
                coerce_str(r.get("source_type")),
                coerce_str(r.get("title")),
                coerce_str(r.get("url")),
            ))
        else:
            cur.execute("""
                INSERT INTO sources(product_id, source_type, title, url)
                VALUES (?,?,?,?)
            """, (
                coerce_str(r.get("product_id")),
                coerce_str(r.get("source_type")),
                coerce_str(r.get("title")),
                coerce_str(r.get("url")),
            ))
        n += 1
    if verbose:
        print(f"  sources: {n} rows upserted")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(csv_dir: Path, db_path: Path, verbose: bool = False):
    print(f"Building {db_path} from CSVs in {csv_dir}/")

    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.executescript(INDEXES)

    # Disable FK checks during bulk load (predecessor/successor may forward-reference)
    conn.execute("PRAGMA foreign_keys = OFF")
    load_manufacturers(conn, read_csv(csv_dir / "manufacturers.csv"), verbose)
    load_families(conn, read_csv(csv_dir / "families.csv"), verbose)
    load_products(conn, read_csv(csv_dir / "products.csv"), verbose)
    load_lineage(conn, read_csv(csv_dir / "lineage.csv"), verbose)
    load_sources(conn, read_csv(csv_dir / "sources.csv"), verbose)
    conn.execute("PRAGMA foreign_keys = ON")

    conn.commit()
    conn.close()

    size_kb = db_path.stat().st_size / 1024
    print(f"\nDone. {db_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build headphones.db from CSVs")
    parser.add_argument("--csv-dir", default="database", help="Directory containing CSV files")
    parser.add_argument("--db", default="database/headphones.db", help="Output SQLite DB path")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    build(
        csv_dir=Path(args.csv_dir),
        db_path=Path(args.db),
        verbose=args.verbose,
    )
