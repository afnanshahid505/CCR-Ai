import json

INPUT_FILE = "discovered_urls.json"      # your noisy discovered URLs
OUTPUT_FILE = "canonical_urls.json"    # clean, usable URLs

VALID_PREFIX = "https://govt.westlaw.com/calregs/Browse/Home/"


def is_canonical_ccr_url(url: str) -> bool:
    return (
        url.startswith(VALID_PREFIX)
        and "guid=" in url
        and " " not in url
    )


def filter_urls():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    canonical_urls = sorted(
        {url for url in urls if is_canonical_ccr_url(url)}
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(canonical_urls, f, indent=2)

    print(f"[DONE] Filtered {len(canonical_urls)} canonical CCR URLs")


if __name__ == "__main__":
    filter_urls()
