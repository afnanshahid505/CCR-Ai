import asyncio
import json
from datetime import datetime, timezone
from crawl4ai import AsyncWebCrawler

INPUT_FILE = "canonical_urls.json"
OUTPUT_FILE = "raw_pages.jsonl"


async def crawl_pages():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        urls = json.load(f)

    async with AsyncWebCrawler(verbose=True) as crawler:
        for url in urls:
            try:
                result = await crawler.arun(
                    url=url,
                    bypass_cache=True
                )

                record = {
                    "url": url,
                    "content": result.markdown,
                    "html": result.html,
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "status": "success"
                }

                with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
                    out.write(json.dumps(record) + "\n")

                print(f"[OK] Crawled: {url}")

            except Exception as e:
                error_record = {
                    "url": url,
                    "error": str(e),
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "status": "failed"
                }

                with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
                    out.write(json.dumps(error_record) + "\n")

                print(f"[FAIL] {url} → {e}")


if __name__ == "__main__":
    asyncio.run(crawl_pages())
