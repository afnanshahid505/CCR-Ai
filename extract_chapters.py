import json
import re
from urllib.parse import urljoin

INPUT_FILE = "raw_division_pages.jsonl"
OUTPUT_FILE = "chapter_urls.json"

# Regex to detect chapter entries in markdown
CHAPTER_PATTERN = re.compile(
    r"\*\s+\[Chapter\s+(\d+(?:\.\d+)?)\.\s+(.*?)\]\((.*?)\)",
    re.IGNORECASE
)


def extract_chapters():
    chapters = []
    seen = set()

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            content = record.get("content")
            if not content:
                continue

            # Try to find chapters
            matches = CHAPTER_PATTERN.findall(content)
            if not matches:
                continue  # Division has no chapters → handled later

            base_url = record["url"]

            for chapter_number, chapter_name, chapter_url in matches:
                full_url = urljoin(base_url, chapter_url)

                key = (record.get("title_number"),
                       record.get("division_number"),
                       chapter_number,
                       full_url)

                if key in seen:
                    continue
                seen.add(key)

                chapters.append({
                    "title_number": record.get("title_number"),
                    "title_name": record.get("title_name"),
                    "division_number": record.get("division_number"),
                    "division_name": record.get("division_name"),
                    "chapter_number": chapter_number,
                    "chapter_name": chapter_name.strip(),
                    "chapter_url": full_url
                })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(chapters, out, indent=2)

    print(f"[DONE] Extracted {len(chapters)} chapters")


if __name__ == "__main__":
    extract_chapters()