import asyncio
import json
from datetime import datetime, timezone
from crawl4ai import AsyncWebCrawler

INPUT_FILE = "discover_divisions.json"
OUTPUT_FILE = "raw_division_pages.jsonl"

# Safety controls
MAX_CONCURRENT = 2          # very safe
DELAY_SECONDS = 2           # pause between requests
MAX_RETRIES = 3


async def crawl_one(crawler, division, semaphore):
    async with semaphore:
        url = division["division_url"]

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                result = await crawler.arun(
                    url=url,
                    bypass_cache=True
                )

                record = {
                    "url": url,
                    "title_number": division["title_number"],
                    "title_name": division["title_name"],
                    "division_number": division["division_number"],
                    "division_name": division["division_name"],
                    "content": result.markdown,
                    "html": result.html,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }

                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(json.dumps(record) + "\n")

                print(f"[OK] {url}")
                await asyncio.sleep(DELAY_SECONDS)
                return

            except Exception as e:
                print(f"[RETRY {attempt}] {url} → {e}")
                await asyncio.sleep(2 * attempt)

        # Failed after retries
        fail_record = {
            "url": url,
            "title_number": division["title_number"],
            "division_number": division["division_number"],
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "failed"
        }

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(fail_record) + "\n")

        print(f"[FAILED] {url}")


async def crawl_divisions():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        divisions = json.load(f)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    async with AsyncWebCrawler(verbose=True) as crawler:
        tasks = [
            crawl_one(crawler, division, semaphore)
            for division in divisions
        ]
        await asyncio.gather(*tasks)

    print("[DONE] Division crawling completed")


if __name__ == "__main__":
    asyncio.run(crawl_divisions())