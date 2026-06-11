"""Scrapes Twenty CRM docs pages and saves them as plain text files in data/raw_docs/."""

import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://docs.twenty.com"

PAGES = [
    "/user-guide/data-model/overview",
    "/user-guide/data-model/capabilities/objects",
    "/user-guide/data-model/how-tos/create-custom-fields",
    "/user-guide/data-model/how-tos/create-custom-objects",
    "/user-guide/data-model/how-tos/create-relation-fields",
    "/user-guide/workflows/overview",
    "/user-guide/workflows/capabilities/workflow-actions",
    "/user-guide/workflows/capabilities/workflow-triggers",
    "/user-guide/workflows/how-tos/crm-automations/closed-won-automations",
]

OUT_DIR = Path(__file__).parent.parent / "data" / "raw_docs"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slug(path: str) -> str:
    return path.strip("/").replace("/", "__")


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    # Mintlify docs put page content inside <main> or an article tag
    main = soup.find("main") or soup.find("article") or soup.body
    if main is None:
        return ""
    # Remove nav, footer, and script noise
    for tag in main.find_all(["nav", "footer", "script", "style", "button"]):
        tag.decompose()
    text = main.get_text(separator="\n")
    # Strip zero-width spaces and other invisible Unicode from Mintlify
    text = re.sub(r"[​‌‍﻿]", "", text)
    # Collapse runs of blank lines to a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def scrape():
    for path in PAGES:
        url = BASE_URL + path
        print(f"Fetching {url} ...", end=" ", flush=True)
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            print(f"FAILED ({r.status_code})")
            continue
        text = extract_text(r.text)
        out_file = OUT_DIR / f"{slug(path)}.txt"
        out_file.write_text(text, encoding="utf-8")
        print(f"saved ({len(text):,} chars) -> {out_file.name}")
        time.sleep(0.5)  # be polite to the server


if __name__ == "__main__":
    scrape()
    print("\nDone.")
