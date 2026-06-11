#!/usr/bin/env python3
"""
verify.py — Pull the headphone data (local OR from GitHub) and verify it's intact.

This is your "does everything work and is the data there?" check. It reads the
five CSVs, builds an in-memory SQLite database, runs integrity checks, and shows
a sample search — proving the full round trip without touching your real DB file.

Usage:
    # Verify local CSVs
    python scripts/verify.py

    # Verify data pulled straight from GitHub (the real test)
    python scripts/verify.py --remote https://raw.githubusercontent.com/USER/headphone-database/main/database

    # Run a quick search against the pulled data
    python scripts/verify.py --remote <base_url> --search "HD 600"
"""

import argparse
import csv
import io
import sqlite3
import sys
import urllib.request
from pathlib import Path

# Make output UTF-8 safe on Windows consoles (prevents UnicodeEncodeError on the
# box-drawing/checkmark characters this script prints).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CSV_FILES = ["manufacturers", "families", "products", "lineage", "sources"]

SCHEMA = """
CREATE TABLE manufacturers (manufacturer_id INTEGER PRIMARY KEY, name TEXT, country TEXT, website TEXT, status TEXT);
CREATE TABLE families (family_id INTEGER PRIMARY KEY, manufacturer_id INTEGER, family_name TEXT, family_type TEXT);
CREATE TABLE products (
    product_id TEXT PRIMARY KEY, family_id INTEGER, manufacturer_id INTEGER,
    model_name TEXT, full_name TEXT, release_year INTEGER, discontinued_year INTEGER,
    status TEXT, category TEXT, design TEXT, driver_type TEXT,
    driver_size_mm TEXT, impedance_ohms TEXT, sensitivity_db TEXT,
    wireless TEXT, anc TEXT, predecessor TEXT, successor TEXT, notes TEXT,
    date_added TEXT, id INTEGER UNIQUE
);
CREATE TABLE lineage (lineage_id INTEGER PRIMARY KEY, predecessor_product_id TEXT, successor_product_id TEXT);
CREATE TABLE sources (source_id INTEGER PRIMARY KEY, product_id TEXT, source_type TEXT, title TEXT, url TEXT);
"""

GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"; DIM = "\033[2m"; RESET = "\033[0m"
OK = f"{GREEN}✓{RESET}"; FAIL = f"{RED}✗{RESET}"; WARN = f"{YELLOW}!{RESET}"


def fetch_csv(source: str, name: str) -> list[dict]:
    """Read one CSV from a local directory or a remote base URL."""
    if source.startswith("http://") or source.startswith("https://"):
        url = f"{source.rstrip('/')}/{name}.csv"
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                text = resp.read().decode("utf-8")
        except Exception as e:
            print(f"  {FAIL} Could not fetch {url}\n      {e}")
            sys.exit(1)
        return list(csv.DictReader(io.StringIO(text)))
    else:
        path = Path(source) / f"{name}.csv"
        if not path.exists():
            print(f"  {FAIL} Missing file: {path}")
            sys.exit(1)
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))


def to_int(v):
    try:
        return int(v) if v not in (None, "") else None
    except (ValueError, TypeError):
        return None


def build_memory_db(source: str) -> tuple[sqlite3.Connection, dict]:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    counts = {}

    for name in CSV_FILES:
        rows = fetch_csv(source, name)
        counts[name] = len(rows)
        if not rows:
            continue
        cols = list(rows[0].keys())
        placeholders = ",".join("?" * len(cols))
        int_cols = {"manufacturer_id", "family_id", "release_year",
                    "discontinued_year", "lineage_id", "source_id"}
        for r in rows:
            vals = [to_int(r[c]) if c in int_cols else (r[c] or None) for c in cols]
            conn.execute(
                f"INSERT OR REPLACE INTO {name} ({','.join(cols)}) VALUES ({placeholders})", vals
            )
    conn.commit()
    return conn, counts


def run_checks(conn: sqlite3.Connection, counts: dict) -> bool:
    print(f"\n  {'Table':<16}{'Rows':>6}")
    print(f"  {DIM}{'-'*22}{RESET}")
    for name in CSV_FILES:
        n = counts.get(name, 0)
        mark = OK if n > 0 else WARN
        print(f"  {mark} {name:<14}{n:>6}")

    print(f"\n  Integrity checks:")
    all_ok = True

    # 1. Products with no manufacturer match
    orphans = conn.execute("""
        SELECT p.product_id FROM products p
        LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
        WHERE m.manufacturer_id IS NULL
    """).fetchall()
    if orphans:
        all_ok = False
        print(f"  {FAIL} {len(orphans)} product(s) reference a missing manufacturer:")
        for o in orphans:
            print(f"        - {o['product_id']}")
    else:
        print(f"  {OK} Every product maps to a known manufacturer")

    # 2. Products with no family match (family_id set but not found)
    fam_orphans = conn.execute("""
        SELECT p.product_id FROM products p
        WHERE p.family_id IS NOT NULL
          AND p.family_id NOT IN (SELECT family_id FROM families)
    """).fetchall()
    if fam_orphans:
        all_ok = False
        print(f"  {FAIL} {len(fam_orphans)} product(s) reference a missing family")
    else:
        print(f"  {OK} Every product's family is valid")

    # 3. Required fields present
    missing = conn.execute("""
        SELECT product_id FROM products
        WHERE product_id IS NULL OR product_id = '' OR model_name IS NULL OR model_name = ''
    """).fetchall()
    if missing:
        all_ok = False
        print(f"  {FAIL} {len(missing)} product(s) missing product_id or model_name")
    else:
        print(f"  {OK} All products have an ID and model name")

    # 4. Duplicate product IDs
    dupes = conn.execute("""
        SELECT product_id, COUNT(*) n FROM products GROUP BY product_id HAVING n > 1
    """).fetchall()
    if dupes:
        all_ok = False
        print(f"  {FAIL} Duplicate product IDs: {', '.join(d['product_id'] for d in dupes)}")
    else:
        print(f"  {OK} No duplicate product IDs")

    # 5. Sources pointing at non-existent products
    src_orphans = conn.execute("""
        SELECT s.source_id FROM sources s
        WHERE s.product_id IS NOT NULL
          AND s.product_id NOT IN (SELECT product_id FROM products)
    """).fetchall()
    if src_orphans:
        print(f"  {WARN} {len(src_orphans)} source(s) point at a product_id not in products "
              f"{DIM}(ok if added later){RESET}")
    else:
        print(f"  {OK} Every source maps to a known product")

    return all_ok


def show_sample(conn: sqlite3.Connection, search: str | None):
    if search:
        rows = conn.execute("""
            SELECT p.full_name, m.name AS mfr, p.release_year, p.design, p.status
            FROM products p LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            WHERE p.full_name LIKE ? OR p.model_name LIKE ? OR p.notes LIKE ?
            ORDER BY p.release_year
        """, tuple([f"%{search}%"] * 3)).fetchall()
        print(f"\n  Search results for '{search}':")
    else:
        rows = conn.execute("""
            SELECT p.full_name, m.name AS mfr, p.release_year, p.design, p.status
            FROM products p LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
            ORDER BY m.name, p.release_year
        """).fetchall()
        print(f"\n  Sample of the data ({len(rows)} products):")

    if not rows:
        print(f"  {DIM}(none){RESET}")
        return
    for r in rows:
        print(f"    • {r['full_name']:<32} {r['mfr']:<13} {r['release_year'] or '?':<6} "
              f"{r['design'] or '':<13} {r['status'] or ''}")


def main():
    parser = argparse.ArgumentParser(description="Verify the headphone data is present and intact")
    parser.add_argument("--remote", metavar="BASE_URL",
                        help="GitHub raw base URL of the /database folder")
    parser.add_argument("--source", default="database",
                        help="Local CSV directory (default: database)")
    parser.add_argument("--search", help="Run a sample search against the pulled data")
    args = parser.parse_args()

    source = args.remote or args.source
    where = "GitHub" if args.remote else "local files"

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  VERIFYING HEADPHONE DATA  ({where})")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Source: {DIM}{source}{RESET}")

    conn, counts = build_memory_db(source)
    ok = run_checks(conn, counts)
    show_sample(conn, args.search)

    print()
    if ok:
        print(f"  {GREEN}━━━ ALL CHECKS PASSED ━━━{RESET}")
        print(f"  {DIM}The data was pulled and is internally consistent.{RESET}\n")
        sys.exit(0)
    else:
        print(f"  {RED}━━━ ISSUES FOUND (see above) ━━━{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
