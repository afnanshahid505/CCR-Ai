import json
from urllib.parse import urljoin

RAW_PAGES_FILE = "raw_pages.jsonl"
OUTPUT_FILE = "division_urls.json"
BASE_URL = "https://govt.westlaw.com"


def extract_division_urls():
    division_urls = set()

    with open(RAW_PAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            url = record.get("url", "")
            content = record.get("content", "")

            # Process only Title pages
            if "/Browse/Home/California/CaliforniaCodeofRegulations" in url:
                for line in content.splitlines():
                    if line.strip().startswith("* [Division"):
                        start = line.find("(") + 1
                        end = line.find(")")
                        rel_url = line[start:end]

                        full_url = urljoin(BASE_URL, rel_url)
                        division_urls.add(full_url)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(sorted(division_urls), out, indent=2)

    print(f"[DONE] Extracted {len(division_urls)} division URLs")


if __name__ == "__main__":
    extract_division_urls()
