#!/usr/bin/env python3
# Copyright 2025 ROS Robotics Companies DB Authors
# Licensed under the Apache License, Version 2.0

"""
parse_companies.py

Fetches the vmayoral/ros-robotics-companies README, parses both the
'Active companies' and 'Acquired/closed/inactive' markdown tables, and
writes the results into a SQLite database (companies.db).

Usage:
    python parse_companies.py [--output companies.db]
"""

import argparse
import re
import sqlite3
import sys
import urllib.request

README_URL = (
    "https://raw.githubusercontent.com/"
    "vmayoral/ros-robotics-companies/main/README.md"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_readme(url: str) -> str:
    print(f"Fetching README from {url} ...")
    with urllib.request.urlopen(url) as resp:
        return resp.read().decode("utf-8")


def strip_markdown_links(text: str) -> str:
    """Replace [label](url) with just label."""
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)


def extract_url(cell: str) -> str | None:
    """Return the first URL found inside a markdown link, or None."""
    m = re.search(r"\[([^\]]*)\]\(([^)]+)\)", cell)
    if m:
        url = m.group(2).strip()
        # skip relative/anchor links
        if url.startswith("http"):
            return url
    return None


def extract_github_url(description: str) -> str | None:
    """
    Return the first github.com URL found in the description cell, or None.
    Prefers links whose label contains 'driver', 'ros', or the org name.
    """
    urls = re.findall(r"https://github\.com/[^\s)\"']+", description)
    if not urls:
        return None
    # prefer a url that looks like a repo/org page (no #fragment)
    for url in urls:
        if "#" not in url:
            return url
    return urls[0]


def parse_year(cell: str) -> int | None:
    text = strip_markdown_links(cell).strip()
    m = re.match(r"(\d{4})", text)
    return int(m.group(1)) if m else None


def parse_table(block: str, status: str) -> list[dict]:
    """
    Parse a markdown table block into a list of company dicts.
    Expected columns: Company | Description | Year Founded
    """
    rows = []
    for line in block.splitlines():
        line = line.strip()
        # skip header and separator rows
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[\s\-|]+\|$", line):
            continue
        if "Company" in line and "Description" in line:
            continue

        cells = [c.strip() for c in line.split("|")]
        # remove empty first/last elements from leading/trailing pipes
        cells = [c for c in cells if c != ""]
        if len(cells) < 3:
            continue

        company_cell, desc_cell, year_cell = cells[0], cells[1], cells[2]

        name = strip_markdown_links(company_cell).strip()
        if not name:
            continue

        company_url = extract_url(company_cell)
        github_url = extract_github_url(desc_cell)
        description = strip_markdown_links(desc_cell).strip()
        # collapse multiple whitespace / footnote markers like [1]
        description = re.sub(r"\[\d+\]", "", description).strip()
        year = parse_year(year_cell)

        rows.append(
            {
                "name": name,
                "url": company_url,
                "description": description,
                "year_founded": year,
                "status": status,
                "github_url": github_url,
            }
        )
    return rows


def split_sections(readme: str) -> tuple[str, str]:
    """
    Return (active_block, inactive_block) by splitting on the
    '### Companies acquired' heading.
    """
    active_marker = "### Active companies"
    inactive_marker = "### Companies acquired"

    i_active = readme.find(active_marker)
    i_inactive = readme.find(inactive_marker)

    if i_active == -1 or i_inactive == -1:
        print(
            "WARNING: Could not find expected section headings. "
            "Attempting full-document parse as active.",
            file=sys.stderr,
        )
        return readme, ""

    active_block = readme[i_active:i_inactive]
    inactive_block = readme[i_inactive:]
    return active_block, inactive_block


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS companies (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    url          TEXT,
    description  TEXT,
    year_founded INTEGER,
    status       TEXT    CHECK(status IN ('active', 'acquired', 'closed', 'inactive')),
    github_url   TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS companies_fts USING fts5(
    name,
    description,
    content='companies',
    content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS companies_ai AFTER INSERT ON companies BEGIN
    INSERT INTO companies_fts(rowid, name, description)
    VALUES (new.id, new.name, new.description);
END;

CREATE TRIGGER IF NOT EXISTS companies_ad AFTER DELETE ON companies BEGIN
    INSERT INTO companies_fts(companies_fts, rowid, name, description)
    VALUES ('delete', old.id, old.name, old.description);
END;

CREATE TRIGGER IF NOT EXISTS companies_au AFTER UPDATE ON companies BEGIN
    INSERT INTO companies_fts(companies_fts, rowid, name, description)
    VALUES ('delete', old.id, old.name, old.description);
    INSERT INTO companies_fts(rowid, name, description)
    VALUES (new.id, new.name, new.description);
END;
"""


def build_database(companies: list[dict], db_path: str) -> None:
    print(f"Writing {len(companies)} companies to {db_path} ...")
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    # Drop and recreate for clean rebuild
    cur.executescript(
        "DROP TABLE IF EXISTS companies_fts;"
        "DROP TRIGGER IF EXISTS companies_ai;"
        "DROP TRIGGER IF EXISTS companies_ad;"
        "DROP TRIGGER IF EXISTS companies_au;"
        "DROP TABLE IF EXISTS companies;"
    )
    cur.executescript(DDL)

    cur.executemany(
        """
        INSERT INTO companies (name, url, description, year_founded, status, github_url)
        VALUES (:name, :url, :description, :year_founded, :status, :github_url)
        """,
        companies,
    )
    con.commit()
    con.close()
    print("Done.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build ROS companies SQLite database.")
    parser.add_argument("--output", default="companies.db", help="Output database path.")
    parser.add_argument("--readme", default=None, help="Local README.md path (skips fetch).")
    args = parser.parse_args()

    if args.readme:
        with open(args.readme, encoding="utf-8") as f:
            readme = f.read()
    else:
        readme = fetch_readme(README_URL)

    active_block, inactive_block = split_sections(readme)

    companies: list[dict] = []
    companies.extend(parse_table(active_block, status="active"))
    companies.extend(parse_table(inactive_block, status="inactive"))

    print(f"Parsed {len(companies)} companies total.")
    build_database(companies, args.output)


if __name__ == "__main__":
    main()
