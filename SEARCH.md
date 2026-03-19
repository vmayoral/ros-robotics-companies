# Interactive Company Search

This PR adds an interactive web-based search interface for the companies
listed in this repository, built entirely on open-source tools.

## How it works

1. `scripts/parse_companies.py` fetches this repository's README, parses
   both the active and acquired/inactive tables, and writes a SQLite
   database (`site/companies.db`) with full-text search support.

2. The database is then exported to a static `companies.json` file at CI
   time, which the frontend fetches directly -- no backend server required.

3. `frontend/index.html` is a single-file, dependency-free frontend that
   loads `companies.json` and renders results as searchable, filterable
   company cards -- no SQL required for end users.

4. `.github/workflows/deploy.yml` rebuilds the database and JSON file
   daily and on every push to `main`, then deploys both to GitHub Pages
   automatically.

## Features

- Full-text search across company names and descriptions
- Filter by status (active / acquired / inactive)
- Filter by founding decade
- Sort alphabetically or by founding year
- Website and GitHub links on each card

## Local testing
```bash
# 1 -- build the database and export to JSON
python scripts/parse_companies.py --output site/companies.db
python - <<'EOF'
import sqlite3, json
con = sqlite3.connect("site/companies.db")
con.row_factory = sqlite3.Row
rows = [dict(r) for r in con.execute("SELECT * FROM companies ORDER BY name")]
json.dump(rows, open("site/companies.json", "w"))
EOF

# 2 -- serve the site
cd site
python -m http.server 8080

# open http://localhost:8080
```

## Enabling on the forked repository

1. Settings -> Pages -> Source: **GitHub Actions**
2. Settings -> Actions -> General -> Workflow permissions: **Read and write**
3. Push -- `deploy.yml` will run automatically and handle the rest.
4. Once the Action completes, the search interface will be live at:
   `https://<your-username>.github.io/ros-robotics-companies/`