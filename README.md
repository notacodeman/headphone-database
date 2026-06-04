# Headphone Database

A scalable, version-controlled headphone catalog backed by CSVs + SQLite.

## Structure

```
headphone-database/
├── database/
│   ├── manufacturers.csv
│   ├── families.csv
│   ├── products.csv
│   ├── lineage.csv
│   ├── sources.csv
│   └── headphones.db          ← generated, do not commit
├── scripts/
│   ├── build_db.py            ← CSV → SQLite
│   ├── query.py               ← Search & filter CLI
│   └── add_item.py            ← Safe insert/update helper
└── docs/
```

## Quick start

```bash
# Build the database from CSVs
python scripts/build_db.py --verbose

# Query all products
python scripts/query.py

# Search
python scripts/query.py --search "HD 600"
python scripts/query.py --manufacturer Sennheiser
python scripts/query.py --design "Open Back" --wireless No
python scripts/query.py --anc Yes --status Active
python scripts/query.py --year-min 2015 --year-max 2023

# Stats
python scripts/query.py --stats

# Lineage
python scripts/query.py --lineage SENN_HD600

# Export results
python scripts/query.py --manufacturer Sony --export sony_products.csv

# Add a new product (interactive)
python scripts/add_item.py product

# Add non-interactively
python scripts/add_item.py product --json '{"product_id":"BEYER_DT990PRO","manufacturer_id":4,...}'
```

## Adding new data

**Preferred workflow**: edit CSVs directly, then rebuild.

```bash
# 1. Edit database/products.csv (or manufacturers, families, etc.)
# 2. Rebuild
python scripts/build_db.py --verbose
# 3. Commit CSVs to git (never commit headphones.db)
```

**Or use add_item.py** for interactive entry — it writes to both DB and CSVs simultaneously.

## Product ID convention

```
MANUFACTURER_MODELSLUG
```
Examples: `SONY_WH1000XM5`, `SENN_HD600`, `BEYER_DT990PRO`, `ATECH_M50X`

Rules:
- Uppercase only
- Letters, digits, underscores
- Manufacturer prefix matches `manufacturers.csv`

## Status values

| Status | Meaning |
|--------|---------|
| Active | Currently sold |
| Discontinued | No longer produced |
| Legacy | Older but still widely used/relevant |
| Legacy Active | Old but still officially available |

## Design values

`Open Back` / `Closed Back` / `Semi-Open` / `In-Ear` / `Bone Conduction`

## Driver type values

`Dynamic` / `Planar Magnetic` / `Electrostatic` / `Hybrid` / `BA` / `Piezoelectric`

## Git notes

Add to `.gitignore`:
```
database/headphones.db
```

Commit only CSVs. The DB is always reproducible via `build_db.py`.
