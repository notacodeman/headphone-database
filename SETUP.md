# Setup: host on GitHub & verify the data

Goal for this stage: get the data living on GitHub and prove you can pull it
back down and search it. No website yet — just confirming the pipeline works.

## 1. Put the project on GitHub

From inside the `headphone-database/` folder:

```bash
git init
git add .
git commit -m "Initial headphone database: CSVs, scripts, schema"
```

Then create an **empty** repo on github.com (no README, no .gitignore — you
already have those), and connect it:

```bash
git remote add origin https://github.com/USER/headphone-database.git
git branch -M main
git push -u origin main
```

Replace `USER` with your GitHub username. The `headphones.db` file is
git-ignored on purpose — it's always rebuildable from the CSVs, so only the
CSVs (the source of truth) get committed.

## 2. Find your raw data URL

Once pushed, your CSVs are publicly readable at:

```
https://raw.githubusercontent.com/USER/headphone-database/main/database
```

That's the base URL for the `/database` folder. Each CSV lives at
`<base>/products.csv`, `<base>/manufacturers.csv`, etc.

## 3. Verify the round trip

This is the moment of truth — pull the data straight from GitHub and check it:

```bash
python scripts/verify.py --remote https://raw.githubusercontent.com/USER/headphone-database/main/database
```

You should see row counts per table, a set of integrity checks (no orphaned
foreign keys, no duplicate IDs, required fields present), and a sample of the
data. A search works too:

```bash
python scripts/verify.py --remote <base_url> --search "HD 600"
```

If every check passes, the data is hosted, pullable, and intact. Done for now.

## 4. Day-to-day workflow from here

```bash
# 1. Edit a CSV (e.g. add a headphone to database/products.csv)
# 2. Rebuild your local DB to sanity-check it
python scripts/build_db.py --verbose
python scripts/query.py --stats

# 3. Push the updated CSVs
git add database/*.csv
git commit -m "Add Beyerdynamic DT 990 Pro"
git push

# 4. (optional) Confirm the live data updated
python scripts/verify.py --remote <base_url>
```

## Note on caching

`raw.githubusercontent.com` caches files for a few minutes (~5 min CDN TTL).
After a push, a verify pull might briefly show the old data before the cache
refreshes — that's expected, not a bug.

## When you're ready for a website

The data layer won't change. A future frontend can either:
- pull these same raw CSVs and search in the browser, or
- migrate `headphones.db` to a queryable host (e.g. Turso) for live SQL.

Either way, GitHub stays the source of truth.
