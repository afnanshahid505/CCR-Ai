import json
import re
from urllib.parse import urljoin

RAW_PAGES_FILE = "raw_pages.jsonl"
OUTPUT_FILE = "discover_divisions.json"
BASE_URL = "https://govt.westlaw.com"


def extract_title_info(markdown: str):
    """
    Extract title number and title name from markdown.
    Example: '# Title 22. Social Security'
    """
    for line in markdown.splitlines():
        if line.startswith("# Title"):
            match = re.match(r"# Title (\d+)\.\s*(.+)", line)
            if match:
                return match.group(1), match.group(2)
    return None, None


def extract_divisions():
    divisions = []

    with open(RAW_PAGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)

            url = record.get("url", "")
            content = record.get("content", "")

            # Only process canonical Title pages
            if (
                "/calregs/Browse/Home/California/CaliforniaCodeofRegulations" in url
                and "guid=" in url
                and "# Title" in content
            ):
                title_number, title_name = extract_title_info(content)

                if not title_number:
                    continue

                for md_line in content.splitlines():
                    md_line = md_line.strip()

                    if md_line.startswith("* [Division"):
                        # Extract division name
                        name_match = re.match(
                            r"\* \[(Division [\d\.]+)\.\s*(.+?)\]\((.+?)\)",
                            md_line
                        )

                        if not name_match:
                            continue

                        division_number = name_match.group(1).replace("Division ", "")
                        division_name = name_match.group(2)
                        rel_url = name_match.group(3)

                        division_url = urljoin(BASE_URL, rel_url)

                        # Keep only canonical CCR URLs
                        if "/calregs/Browse/Home/" not in division_url or "guid=" not in division_url:
                            continue

                        divisions.append({
                            "title_number": title_number,
                            "title_name": title_name,
                            "division_number": division_number,
                            "division_name": division_name,
                            "division_url": division_url
                        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(divisions, out, indent=2)

    print(f"[DONE] Extracted {len(divisions)} structured divisions")


if __name__ == "__main__":
    extract_divisions()
