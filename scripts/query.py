#!/usr/bin/env python3
"""
query.py — Search and filter the headphone database

Usage examples:
    python scripts/query.py --search "HD 600"
    python scripts/query.py --manufacturer Sennheiser
    python scripts/query.py --design "Open Back" --wireless No
    python scripts/query.py --anc Yes --status Active
    python scripts/query.py --driver Planar
    python scripts/query.py --year-min 2015 --year-max 2023
    python scripts/query.py --stats
    python scripts/query.py --lineage SENN_HD600
    python scripts/query.py --list-manufacturers
    python scripts/query.py --export results.csv
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

DEFAULT_DB = "database/headphones.db"


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def connect(db_path: str) -> sqlite3.Connection:
    p = Path(db_path)
    if not p.exists():
        sys.exit(f"[ERROR] Database not found: {db_path}\nRun: python scripts/build_db.py")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------

PRODUCT_SELECT = """
    SELECT
        p.product_id,
        m.name        AS manufacturer,
        f.family_name AS family,
        p.model_name,
        p.full_name,
        p.release_year,
        p.discontinued_year,
        p.status,
        p.category,
        p.design,
        p.driver_type,
        p.wireless,
        p.anc,
        p.predecessor,
        p.successor,
        p.notes
    FROM products p
    LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
    LEFT JOIN families      f ON p.family_id       = f.family_id
"""


def search_products(conn, args) -> list[sqlite3.Row]:
    """Build and run a filtered product query from the CLI args (brand, design, driver, year, etc.).
    Returns matching rows so the print/export helpers can format them for the terminal or a file."""
    where = []
    params = []

    if args.search:
        where.append("(p.full_name LIKE ? OR p.model_name LIKE ? OR p.notes LIKE ?)")
        q = f"%{args.search}%"
        params += [q, q, q]

    if args.manufacturer:
        where.append("m.name LIKE ?")
        params.append(f"%{args.manufacturer}%")

    if args.design:
        where.append("p.design LIKE ?")
        params.append(f"%{args.design}%")

    if args.driver:
        where.append("p.driver_type LIKE ?")
        params.append(f"%{args.driver}%")

    if args.wireless:
        where.append("p.wireless = ?")
        params.append(args.wireless)

    if args.anc:
        where.append("p.anc = ?")
        params.append(args.anc)

    if args.status:
        where.append("p.status LIKE ?")
        params.append(f"%{args.status}%")

    if args.category:
        where.append("p.category LIKE ?")
        params.append(f"%{args.category}%")

    if args.year_min:
        where.append("p.release_year >= ?")
        params.append(args.year_min)

    if args.year_max:
        where.append("p.release_year <= ?")
        params.append(args.year_max)

    if args.family:
        where.append("f.family_name LIKE ?")
        params.append(f"%{args.family}%")

    sql = PRODUCT_SELECT
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY m.name, p.release_year, p.model_name"

    return conn.execute(sql, params).fetchall()


def get_lineage(conn, product_id: str):
    """Walk the predecessor/successor chain for one product to assemble its full ancestry and
    descendants. Used to print a model's place in its family line."""
    """Return the full chain: ancestors → product → descendants."""
    ancestors = []
    descendants = []

    # Walk backwards
    pid = product_id
    seen = set()
    while True:
        row = conn.execute(
            "SELECT predecessor_product_id FROM lineage WHERE successor_product_id = ?", (pid,)
        ).fetchone()
        if not row or row[0] in seen:
            break
        seen.add(row[0])
        ancestors.insert(0, row[0])
        pid = row[0]

    # Walk forward
    pid = product_id
    seen = set()
    while True:
        row = conn.execute(
            "SELECT successor_product_id FROM lineage WHERE predecessor_product_id = ?", (pid,)
        ).fetchone()
        if not row or row[0] in seen:
            break
        seen.add(row[0])
        descendants.append(row[0])
        pid = row[0]

    return ancestors, descendants


def get_stats(conn) -> dict:
    """Compute summary statistics across the whole catalog (counts by brand, driver, status, year).
    Returns a dict the stats printer turns into the overview shown with the --stats flag."""
    stats = {}
    stats["total_products"] = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    stats["total_manufacturers"] = conn.execute("SELECT COUNT(*) FROM manufacturers").fetchone()[0]
    stats["total_families"] = conn.execute("SELECT COUNT(*) FROM families").fetchone()[0]

    stats["by_status"] = conn.execute(
        "SELECT status, COUNT(*) AS n FROM products GROUP BY status ORDER BY n DESC"
    ).fetchall()

    stats["by_design"] = conn.execute(
        "SELECT design, COUNT(*) AS n FROM products GROUP BY design ORDER BY n DESC"
    ).fetchall()

    stats["by_driver"] = conn.execute(
        "SELECT driver_type, COUNT(*) AS n FROM products GROUP BY driver_type ORDER BY n DESC"
    ).fetchall()

    stats["by_manufacturer"] = conn.execute(
        """SELECT m.name, COUNT(*) AS n
           FROM products p JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
           GROUP BY m.name ORDER BY n DESC"""
    ).fetchall()

    stats["wireless_anc"] = conn.execute(
        """SELECT
             SUM(CASE WHEN wireless='Yes' THEN 1 ELSE 0 END) AS wireless_count,
             SUM(CASE WHEN anc='Yes'      THEN 1 ELSE 0 END) AS anc_count
           FROM products"""
    ).fetchone()

    stats["by_decade"] = conn.execute(
        """SELECT (release_year / 10 * 10) AS decade, COUNT(*) AS n
           FROM products WHERE release_year IS NOT NULL
           GROUP BY decade ORDER BY decade"""
    ).fetchall()

    return stats


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def fmt_row(r: sqlite3.Row) -> str:
    disc = f"→{r['discontinued_year']}" if r["discontinued_year"] else ""
    year = f"{r['release_year']}{disc}" if r["release_year"] else "?"
    wireless = "📶" if r["wireless"] == "Yes" else "  "
    anc = "🔇" if r["anc"] == "Yes" else "  "
    return (
        f"  {wireless}{anc} [{r['product_id']:<22}] "
        f"{r['full_name'] or r['model_name']:<35} "
        f"{r['manufacturer']:<14} "
        f"{r['design'] or '':<13} "
        f"{r['driver_type'] or '':<14} "
        f"{year:<10} "
        f"{r['status'] or ''}"
    )


def print_results(rows: list[sqlite3.Row]):
    if not rows:
        print("No results found.")
        return
    print(f"\nFound {len(rows)} result(s):\n")
    header = (
        f"  {'':4} {'ID':<22} {'Name':<35} {'Brand':<14} "
        f"{'Design':<13} {'Driver':<14} {'Year':<10} Status"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))
    for r in rows:
        print(fmt_row(r))
    print()


def print_stats(stats: dict):
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  HEADPHONE DATABASE STATS")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  Products:      {stats['total_products']}")
    print(f"  Manufacturers: {stats['total_manufacturers']}")
    print(f"  Families:      {stats['total_families']}")

    wac = stats["wireless_anc"]
    print(f"  Wireless:      {wac[0]}")
    print(f"  ANC:           {wac[1]}")

    print("\n  By Manufacturer:")
    for row in stats["by_manufacturer"]:
        print(f"    {row[0]:<20} {row[1]}")

    print("\n  By Design:")
    for row in stats["by_design"]:
        print(f"    {row[0] or 'Unknown':<20} {row[1]}")

    print("\n  By Driver Type:")
    for row in stats["by_driver"]:
        print(f"    {row[0] or 'Unknown':<20} {row[1]}")

    print("\n  By Status:")
    for row in stats["by_status"]:
        print(f"    {row[0] or 'Unknown':<20} {row[1]}")

    print("\n  By Decade Released:")
    for row in stats["by_decade"]:
        decade = f"{row[0]}s" if row[0] else "Unknown"
        bar = "█" * row[1]
        print(f"    {decade:<10} {bar:<30} {row[1]}")

    print()


def print_lineage(product_id: str, ancestors: list, descendants: list):
    print(f"\n  Lineage chain for {product_id}:")
    all_ids = ancestors + [product_id] + descendants
    for i, pid in enumerate(all_ids):
        marker = "► " if pid == product_id else "  "
        connector = "  " if i == 0 else "↓ "
        print(f"    {connector}{marker}{pid}")
    print()


def export_csv(rows: list[sqlite3.Row], path: str):
    if not rows:
        print("Nothing to export.")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows([dict(r) for r in rows])
    print(f"Exported {len(rows)} rows to {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """CLI entry point: parse the query/stats/lineage/export flags and dispatch to the matching
    helper, then print or save the results. This is what runs when query.py is invoked directly."""
    parser = argparse.ArgumentParser(description="Query the headphone database")
    parser.add_argument("--db", default=DEFAULT_DB)

    # Filters
    parser.add_argument("--search", "-s", help="Full-text search on name/notes")
    parser.add_argument("--manufacturer", "-m", help="Filter by manufacturer name")
    parser.add_argument("--design", "-d", help="Filter by design (Open Back, Closed Back…)")
    parser.add_argument("--driver", help="Filter by driver type (Dynamic, Planar…)")
    parser.add_argument("--wireless", choices=["Yes", "No"])
    parser.add_argument("--anc", choices=["Yes", "No"])
    parser.add_argument("--status", help="Filter by status (Active, Discontinued…)")
    parser.add_argument("--category", help="Filter by category (Headphone, IEM…)")
    parser.add_argument("--family", "-f", help="Filter by family name")
    parser.add_argument("--year-min", type=int)
    parser.add_argument("--year-max", type=int)

    # Actions
    parser.add_argument("--stats", action="store_true", help="Show database statistics")
    parser.add_argument("--lineage", metavar="PRODUCT_ID", help="Show lineage chain for a product")
    parser.add_argument("--list-manufacturers", action="store_true")
    parser.add_argument("--export", metavar="FILE.csv", help="Export results to CSV")

    args = parser.parse_args()

    conn = connect(args.db)

    if args.stats:
        print_stats(get_stats(conn))

    elif args.lineage:
        ancestors, descendants = get_lineage(conn, args.lineage)
        print_lineage(args.lineage, ancestors, descendants)

    elif args.list_manufacturers:
        rows = conn.execute(
            "SELECT name, country, status FROM manufacturers ORDER BY name"
        ).fetchall()
        print(f"\n  {'Name':<20} {'Country':<15} Status")
        print("  " + "-" * 45)
        for r in rows:
            print(f"  {r[0]:<20} {r[1] or '':<15} {r[2] or ''}")
        print()

    else:
        # Default: search/filter products
        has_filter = any([
            args.search, args.manufacturer, args.design, args.driver,
            args.wireless, args.anc, args.status, args.category,
            args.year_min, args.year_max, args.family
        ])
        if not has_filter:
            # No filters → show all
            rows = conn.execute(
                PRODUCT_SELECT + " ORDER BY m.name, p.release_year"
            ).fetchall()
        else:
            rows = search_products(conn, args)

        print_results(rows)
        if args.export and rows:
            export_csv(rows, args.export)

    conn.close()


if __name__ == "__main__":
    main()
