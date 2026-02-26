import json
import re
from urllib.parse import urljoin

INPUT_FILE = "raw_division_pages.jsonl"
OUTPUT_FILE = "article_urls.json"

# Regex to match Article links in markdown
# Example:
# * [Article 1. General](https://govt.westlaw.com/...)
article_pattern = re.compile(
    r"\*\s+\[Article\s+([\dA-Za-z\.]+)\.\s+(.*?)\]\((.*?)\)"
)

articles = []
skipped_pages = 0

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)

        content = record.get("content")
        if not content:
            skipped_pages += 1
            continue  # skip empty / failed pages

        base_url = record.get("url")

        title_number = record.get("title_number")
        title_name = record.get("title_name")
        division_number = record.get("division_number")
        division_name = record.get("division_name")

        for match in article_pattern.finditer(content):
            article_number = match.group(1).strip()
            article_name = match.group(2).strip()
            raw_url = match.group(3).strip()

            article_url = urljoin(base_url, raw_url)

            articles.append({
                "title_number": title_number,
                "title_name": title_name,
                "division_number": division_number,
                "division_name": division_name,
                "article_number": article_number,
                "article_name": article_name,
                "url": article_url
            })

# Write output
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, indent=2, ensure_ascii=False)

print(f"[DONE] Extracted {len(articles)} articles")
print(f"[INFO] Skipped {skipped_pages} pages with no content")