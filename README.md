# The Headphone Archive

A catalog of over-ear and on-ear headphones, live at [headphones.codeman.club](https://headphones.codeman.club).
Plain HTML, CSS and JavaScript on Cloudflare Pages, with Pages Functions and a D1 database. No build step.

## How it fits together

- **D1 is the live data.** The public pages read it through `/api/*`, and the admin page edits it.
- **The CSVs in `database/` are the backup and seed.** *Reset from CSV* on the admin page wipes the D1
  catalog and reloads it from the CSVs on GitHub, so it overwrites any edits made since.
- **Admin is protected by Cloudflare Access**, not by code. The Access app covers exactly two paths,
  `/admin` and `/api/admin`, so every admin feature lives on `admin.html` and under `functions/api/admin/`.

## Files

```
site/                     Static pages (the Pages output directory)
  shared.css              Colour tokens, reset, focus outlines — used by every page
  shared.js               escapeHtml() and formatPrice() — used by every page
  index.html              The archive: search, filters, sortable/resizable table, compare, CSV export
  brands.html             Every brand, with search, country and A–Z filters
  brand.html              One brand: summary stats, design/driver breakdown, products by decade
  suggest.html            Public form for suggesting a correction
  admin.html              Catalog editor, suggestion review and suggestion log (behind Access)

functions/                Cloudflare Pages Functions (D1 binding: DB)
  schema.sql              Tables that only exist in D1: suggestions, product_history
  api/catalog.js          GET  all products with brand names
  api/brands.js           GET  all brands, or ?id=N for one brand and its products
  api/suggest.js          POST a suggestion from suggest.html
  api/admin/products.js   GET/POST/DELETE products (POST saves a history snapshot first)
  api/admin/history.js    GET  a product's saved edits
  api/admin/suggestions.js GET all suggestions, POST accept/reject/reopen
  api/admin/import.js     POST wipe and reload the catalog from the GitHub CSVs

database/                 CSV backup of the catalog
scripts/                  Local command-line tools (optional, work on the CSVs)
```

## Setting up D1

1. Bind the D1 database to the Pages project as `DB`.
2. Run `functions/schema.sql` in the D1 console (creates `suggestions` and `product_history`).
3. Open `/admin` and press *Reset from CSV* once to create and fill the catalog tables.

## Local tools

These work on the CSVs, not on D1. Run them from the repo root.

```bash
python scripts/build_db.py --verbose        # CSVs -> database/headphones.db (git-ignored)
python scripts/query.py --search "HD 600"   # search, filter, --stats, --lineage SENN_HD600
python scripts/add_item.py product          # add or update a product, then rewrite the CSV
python scripts/verify.py                    # integrity checks on the CSVs (--remote <url> for GitHub)
```

`scripts/_generate_data.py` is the script that first generated the CSVs. The CSVs have been edited
directly since, so running it now would overwrite those edits.

## Data conventions

Product IDs are `BRAND_MODEL` in upper case with digits and underscores, e.g. `SONY_WH1000XM5`,
`SENN_HD600`.

| Field | Values |
|-------|--------|
| status | Active, Discontinued, Legacy Active |
| design | Open Back, Closed Back, Semi-Open |
| fit | Over-Ear, On-Ear |
| driver_type | Dynamic, Planar Magnetic, Electrostatic, Ribbon, AMT, Hybrid |
| category | Headphone, Studio, Gaming |
| sound_signature | Neutral, Warm Neutral, Neutral Bright, Warm, Bright, Analytical, V-Shaped, U-Shaped, Bassy, Dark |
