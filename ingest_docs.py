import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm

DOC_URLS = {
    # Core DML
    "sql-select": "https://www.postgresql.org/docs/16/sql-select.html",
    "sql-insert": "https://www.postgresql.org/docs/16/sql-insert.html",
    "sql-update": "https://www.postgresql.org/docs/16/sql-update.html",
    "sql-delete": "https://www.postgresql.org/docs/16/sql-delete.html",
    "sql-merge": "https://www.postgresql.org/docs/16/sql-merge.html",

    # DDL
    "sql-createtable": "https://www.postgresql.org/docs/16/sql-createtable.html",
    "sql-altertable": "https://www.postgresql.org/docs/16/sql-altertable.html",
    "sql-droptable": "https://www.postgresql.org/docs/16/sql-droptable.html",
    "sql-createview": "https://www.postgresql.org/docs/16/sql-createview.html",
    "sql-createindex": "https://www.postgresql.org/docs/16/sql-createindex.html",
    "sql-dropindex": "https://www.postgresql.org/docs/16/sql-dropindex.html",

    # Query Analysis & Maintenance
    "sql-explain": "https://www.postgresql.org/docs/16/sql-explain.html",
    "sql-analyze": "https://www.postgresql.org/docs/16/sql-analyze.html",
    "sql-vacuum": "https://www.postgresql.org/docs/16/sql-vacuum.html",

    # Transactions
    "sql-begin": "https://www.postgresql.org/docs/16/sql-begin.html",
    "sql-commit": "https://www.postgresql.org/docs/16/sql-commit.html",
    "sql-rollback": "https://www.postgresql.org/docs/16/sql-rollback.html",
    "sql-savepoint": "https://www.postgresql.org/docs/16/sql-savepoint.html",
    "sql-set-transaction": "https://www.postgresql.org/docs/16/sql-set-transaction.html",

    # Security
    "sql-grant": "https://www.postgresql.org/docs/16/sql-grant.html",
    "sql-revoke": "https://www.postgresql.org/docs/16/sql-revoke.html",
    "sql-createrole": "https://www.postgresql.org/docs/16/sql-createrole.html",
    "sql-alterrole": "https://www.postgresql.org/docs/16/sql-alterrole.html",

    # Database Management
    "sql-createdatabase": "https://www.postgresql.org/docs/16/sql-createdatabase.html",
    "sql-dropdatabase": "https://www.postgresql.org/docs/16/sql-dropdatabase.html",

    # Utilities
    "sql-copy": "https://www.postgresql.org/docs/16/sql-copy.html",
    "sql-truncate": "https://www.postgresql.org/docs/16/sql-truncate.html",
    "sql-set": "https://www.postgresql.org/docs/16/sql-set.html",
    "sql-show": "https://www.postgresql.org/docs/16/sql-show.html",
    "sql-refreshmaterializedview": "https://www.postgresql.org/docs/16/sql-refreshmaterializedview.html",

    # Concepts
    "indexes": "https://www.postgresql.org/docs/16/indexes.html",
    "indexes-partial": "https://www.postgresql.org/docs/16/indexes-partial.html",
    "ddl-constraints": "https://www.postgresql.org/docs/16/ddl-constraints.html",
    "mvcc": "https://www.postgresql.org/docs/16/mvcc.html",
    "runtime-config": "https://www.postgresql.org/docs/16/runtime-config.html",
}

OUTPUT_DIR = "data/raw_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_main_content(html):
    soup = BeautifulSoup(html, "lxml")

    # Main documentation content
    content_div = soup.find("div", {"id": "docContent"})
    if not content_div:
        return None

    sections = []
    current_section = {"title": "Introduction", "text": ""}

    for tag in content_div.find_all(["h1", "h2", "h3", "p", "pre"]):
        if tag.name in ["h1", "h2", "h3"]:
            if current_section["text"].strip():
                sections.append(current_section)
            current_section = {
                "title": tag.get_text(strip=True),
                "text": ""
            }
        elif tag.name == "pre":
            code = tag.get_text()
            current_section["text"] += f"\n\nCODE:\n{code}\n"
        else:
            current_section["text"] += tag.get_text(strip=True) + "\n"

    if current_section["text"].strip():
        sections.append(current_section)

    return sections


def ingest():
    for doc_name, url in tqdm(DOC_URLS.items()):
        print(f"\nFetching {doc_name}")
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
        
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {doc_name}: {e}")
            continue


        sections = extract_main_content(response.text)
        if not sections:
            print(f"Failed to parse {doc_name}")
            continue

        doc_data = {
            "doc_name": doc_name,
            "url": url,
            "sections": sections
        }

        output_path = os.path.join(OUTPUT_DIR, f"{doc_name}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(doc_data, f, indent=2, ensure_ascii=False)

        print(f" Saved {output_path}")


if __name__ == "__main__":
    ingest()
