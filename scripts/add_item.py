#!/usr/bin/env python3
"""
add_item.py — Safely insert or update records in headphones.db AND sync back to CSVs.

Usage:
    python scripts/add_item.py product
    python scripts/add_item.py manufacturer
    python scripts/add_item.py family
    python scripts/add_item.py lineage
    python scripts/add_item.py source

    # Non-interactive (JSON):
    python scripts/add_item.py product --json '{"product_id":"BEYER_DT990","manufacturer_id":4,...}'

    # From file:
    python scripts/add_item.py product --file new_product.json
"""

import argparse
import csv
import json
import re
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
CSV_DIR = Path("database")

# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

VALID_STATUS   = {"Active", "Discontinued", "Legacy", "Legacy Active"}
VALID_DESIGN   = {"Open Back", "Closed Back", "Semi-Open", "In-Ear", "Bone Conduction"}
VALID_DRIVER   = {"Dynamic", "Planar Magnetic", "Electrostatic", "Hybrid", "BA", "Piezoelectric"}
VALID_YESNO    = {"Yes", "No"}


def validate_product(data: dict, conn: sqlite3.Connection) -> list[str]:
    """Validate one product dict against the categorical rules and foreign-key references before
    it is written. Returns a list of human-readable error strings (empty means the row is valid)."""
    errors = []
    if not data.get("product_id"):
        errors.append("product_id is required")
    elif not re.match(r'^[A-Z0-9_]+$', data["product_id"]):
        errors.append("product_id must be uppercase letters, digits, underscores only (e.g. SONY_WH1000XM5)")

    if not data.get("model_name"):
        errors.append("model_name is required")

    if data.get("status") and data["status"] not in VALID_STATUS:
        errors.append(f"status must be one of: {VALID_STATUS}")

    if data.get("design") and data["design"] not in VALID_DESIGN:
        errors.append(f"design must be one of: {VALID_DESIGN}")

    if data.get("driver_type") and data["driver_type"] not in VALID_DRIVER:
        errors.append(f"driver_type must be one of: {VALID_DRIVER}")

    if data.get("wireless") and data["wireless"] not in VALID_YESNO:
        errors.append("wireless must be Yes or No")

    if data.get("anc") and data["anc"] not in VALID_YESNO:
        errors.append("anc must be Yes or No")

    if data.get("release_year"):
        try:
            y = int(data["release_year"])
            if not (1900 <= y <= 2100):
                errors.append("release_year seems out of range")
        except ValueError:
            errors.append("release_year must be an integer")

    if data.get("manufacturer_id"):
        row = conn.execute(
            "SELECT 1 FROM manufacturers WHERE manufacturer_id=?", (data["manufacturer_id"],)
        ).fetchone()
        if not row:
            errors.append(f"manufacturer_id {data['manufacturer_id']} not found in manufacturers table")

    return errors


# ---------------------------------------------------------------------------
# Interactive prompts
# ---------------------------------------------------------------------------

def prompt(label: str, required=False, choices=None, default=None) -> str:
    hint = ""
    if choices:
        hint = f" [{'/'.join(choices)}]"
    if default:
        hint += f" (default: {default})"
    while True:
        val = input(f"  {label}{hint}: ").strip()
        if not val and default:
            return default
        if not val and required:
            print("    ✗ Required. Please enter a value.")
            continue
        if choices and val and val not in choices:
            print(f"    ✗ Must be one of: {', '.join(choices)}")
            continue
        return val


def prompt_product(conn) -> dict:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ADD PRODUCT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Show existing manufacturers for reference
    mfrs = conn.execute("SELECT manufacturer_id, name FROM manufacturers ORDER BY name").fetchall()
    print("\n  Known manufacturers:")
    for m in mfrs:
        print(f"    [{m[0]}] {m[1]}")

    data = {}
    data["product_id"]        = prompt("product_id (e.g. BEYER_DT990PRO)", required=True)
    data["manufacturer_id"]   = prompt("manufacturer_id", required=True)
    data["family_id"]         = prompt("family_id (optional)")
    data["model_name"]        = prompt("model_name (e.g. DT 990 Pro)", required=True)
    data["full_name"]         = prompt("full_name (e.g. Beyerdynamic DT 990 Pro)")
    data["release_year"]      = prompt("release_year (e.g. 2005)")
    data["discontinued_year"] = prompt("discontinued_year (if applicable)")
    data["status"]            = prompt("status", choices=sorted(VALID_STATUS))
    data["category"]          = prompt("category (Headphone/IEM/Gaming)", default="Headphone")
    data["design"]            = prompt("design", choices=sorted(VALID_DESIGN))
    data["driver_type"]       = prompt("driver_type", choices=sorted(VALID_DRIVER))
    data["wireless"]          = prompt("wireless", choices=["Yes", "No"], default="No")
    data["anc"]               = prompt("anc", choices=["Yes", "No"], default="No")
    data["predecessor"]       = prompt("predecessor product_id (optional)")
    data["successor"]         = prompt("successor product_id (optional)")
    data["notes"]             = prompt("notes (optional)")

    return {k: v for k, v in data.items() if v != ""}


def prompt_manufacturer() -> dict:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ADD MANUFACTURER")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    data = {}
    data["name"]    = prompt("name", required=True)
    data["country"] = prompt("country")
    data["website"] = prompt("website")
    data["status"]  = prompt("status", choices=["Active", "Legacy", "Defunct"], default="Active")
    return {k: v for k, v in data.items() if v != ""}


def prompt_family(conn) -> dict:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ADD FAMILY")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    mfrs = conn.execute("SELECT manufacturer_id, name FROM manufacturers ORDER BY name").fetchall()
    print("\n  Known manufacturers:")
    for m in mfrs:
        print(f"    [{m[0]}] {m[1]}")
    data = {}
    data["manufacturer_id"] = prompt("manufacturer_id", required=True)
    data["family_name"]     = prompt("family_name (e.g. HD, WH, Fidelio)", required=True)
    data["family_type"]     = prompt("family_type", default="Headphone")
    return {k: v for k, v in data.items() if v != ""}


def prompt_lineage() -> dict:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ADD LINEAGE ENTRY")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    data = {}
    data["predecessor_product_id"] = prompt("predecessor_product_id", required=True)
    data["successor_product_id"]   = prompt("successor_product_id", required=True)
    return data


def prompt_source() -> dict:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  ADD SOURCE")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    data = {}
    data["product_id"]  = prompt("product_id", required=True)
    data["source_type"] = prompt("source_type (Official Page/Press Release/Retail/Manual)")
    data["title"]       = prompt("title")
    data["url"]         = prompt("url")
    return {k: v for k, v in data.items() if v != ""}


# ---------------------------------------------------------------------------
# DB + CSV writers
# ---------------------------------------------------------------------------

def upsert_product(conn, data: dict):
    """Insert or update a single product in the local SQLite DB, keyed by product_id. This is the
    write half of add_item; sync_csv_products mirrors the result back out to the CSV afterwards."""
    errors = validate_product(data, conn)
    if errors:
        print("\n  ✗ Validation errors:")
        for e in errors:
            print(f"    • {e}")
        sys.exit(1)

    conn.execute("""
        INSERT INTO products(
            product_id, family_id, manufacturer_id,
            model_name, full_name, release_year, discontinued_year,
            status, category, design, driver_type,
            wireless, anc, predecessor, successor, notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(product_id) DO UPDATE SET
            family_id=excluded.family_id, manufacturer_id=excluded.manufacturer_id,
            model_name=excluded.model_name, full_name=excluded.full_name,
            release_year=excluded.release_year, discontinued_year=excluded.discontinued_year,
            status=excluded.status, category=excluded.category,
            design=excluded.design, driver_type=excluded.driver_type,
            wireless=excluded.wireless, anc=excluded.anc,
            predecessor=excluded.predecessor, successor=excluded.successor,
            notes=excluded.notes
    """, (
        data.get("product_id"), data.get("family_id") or None, data.get("manufacturer_id"),
        data.get("model_name"), data.get("full_name"),
        data.get("release_year") or None, data.get("discontinued_year") or None,
        data.get("status"), data.get("category"), data.get("design"), data.get("driver_type"),
        data.get("wireless", "No"), data.get("anc", "No"),
        data.get("predecessor") or None, data.get("successor") or None,
        data.get("notes"),
    ))
    conn.commit()
    sync_csv_products(conn)
    print(f"\n  ✓ Product '{data['product_id']}' saved.")


def upsert_manufacturer(conn, data: dict):
    cur = conn.execute(
        "INSERT INTO manufacturers(name, country, website, status) VALUES (?,?,?,?) "
        "ON CONFLICT(name) DO UPDATE SET country=excluded.country, website=excluded.website, status=excluded.status "
        "RETURNING manufacturer_id",
        (data.get("name"), data.get("country"), data.get("website"), data.get("status", "Active"))
    )
    conn.commit()
    sync_csv_manufacturers(conn)
    print(f"\n  ✓ Manufacturer '{data['name']}' saved.")


def upsert_family(conn, data: dict):
    conn.execute(
        "INSERT INTO families(manufacturer_id, family_name, family_type) VALUES (?,?,?)",
        (data.get("manufacturer_id"), data.get("family_name"), data.get("family_type"))
    )
    conn.commit()
    sync_csv_families(conn)
    print(f"\n  ✓ Family '{data['family_name']}' saved.")


def upsert_lineage(conn, data: dict):
    conn.execute(
        "INSERT OR IGNORE INTO lineage(predecessor_product_id, successor_product_id) VALUES (?,?)",
        (data.get("predecessor_product_id"), data.get("successor_product_id"))
    )
    conn.commit()
    sync_csv_lineage(conn)
    print(f"\n  ✓ Lineage entry saved.")


def upsert_source(conn, data: dict):
    conn.execute(
        "INSERT INTO sources(product_id, source_type, title, url) VALUES (?,?,?,?)",
        (data.get("product_id"), data.get("source_type"), data.get("title"), data.get("url"))
    )
    conn.commit()
    sync_csv_sources(conn)
    print(f"\n  ✓ Source saved.")


# ---------------------------------------------------------------------------
# CSV sync (DB → CSV)
# ---------------------------------------------------------------------------

def sync_csv_products(conn):
    """Export the products table back to products.csv with the full canonical column set, in the
    same column order _generate_data.py uses. Keeps the CSV backup in step with local DB edits."""
    rows = conn.execute(
        "SELECT product_id, family_id, manufacturer_id, model_name, full_name, "
        "release_year, discontinued_year, status, category, design, driver_type, "
        "driver_size_mm, impedance_ohms, sensitivity_db, wireless, anc, "
        "predecessor, successor, notes, date_added, fit, "
        "msrp_usd, sound_signature, connector_type, detachable_cable, weight_g "
        "FROM products ORDER BY product_id"
    ).fetchall()
    _write_csv(CSV_DIR / "products.csv", [
        "product_id","family_id","manufacturer_id","model_name","full_name",
        "release_year","discontinued_year","status","category","design","driver_type",
        "driver_size_mm","impedance_ohms","sensitivity_db","wireless","anc",
        "predecessor","successor","notes","date_added","fit",
        "msrp_usd","sound_signature","connector_type","detachable_cable","weight_g"
    ], rows)


def sync_csv_manufacturers(conn):
    rows = conn.execute(
        "SELECT manufacturer_id, name, country, website, status FROM manufacturers ORDER BY manufacturer_id"
    ).fetchall()
    _write_csv(CSV_DIR / "manufacturers.csv", ["manufacturer_id","name","country","website","status"], rows)


def sync_csv_families(conn):
    rows = conn.execute(
        "SELECT family_id, manufacturer_id, family_name, family_type FROM families ORDER BY family_id"
    ).fetchall()
    _write_csv(CSV_DIR / "families.csv", ["family_id","manufacturer_id","family_name","family_type"], rows)


def sync_csv_lineage(conn):
    rows = conn.execute(
        "SELECT lineage_id, predecessor_product_id, successor_product_id FROM lineage ORDER BY lineage_id"
    ).fetchall()
    _write_csv(CSV_DIR / "lineage.csv", ["lineage_id","predecessor_product_id","successor_product_id"], rows)


def sync_csv_sources(conn):
    rows = conn.execute(
        "SELECT source_id, product_id, source_type, title, url FROM sources ORDER BY source_id"
    ).fetchall()
    _write_csv(CSV_DIR / "sources.csv", ["source_id","product_id","source_type","title","url"], rows)


def _write_csv(path: Path, headers: list, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows([[r[h] if hasattr(r, '__getitem__') else r[i] for i, h in enumerate(headers)] for r in rows])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Add/update headphone database records")
    parser.add_argument("table", choices=["product","manufacturer","family","lineage","source"])
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--json", help="JSON string of data (non-interactive)")
    parser.add_argument("--file", help="JSON file of data (non-interactive)")
    args = parser.parse_args()

    p = Path(args.db)
    if not p.exists():
        sys.exit(f"[ERROR] Database not found: {args.db}\nRun: python scripts/build_db.py")

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # Load data
    data = None
    if args.json:
        data = json.loads(args.json)
    elif args.file:
        data = json.loads(Path(args.file).read_text())

    # Dispatch
    if args.table == "product":
        if data is None:
            data = prompt_product(conn)
        upsert_product(conn, data)

    elif args.table == "manufacturer":
        if data is None:
            data = prompt_manufacturer()
        upsert_manufacturer(conn, data)

    elif args.table == "family":
        if data is None:
            data = prompt_family(conn)
        upsert_family(conn, data)

    elif args.table == "lineage":
        if data is None:
            data = prompt_lineage()
        upsert_lineage(conn, data)

    elif args.table == "source":
        if data is None:
            data = prompt_source()
        upsert_source(conn, data)

    conn.close()


if __name__ == "__main__":
    main()
