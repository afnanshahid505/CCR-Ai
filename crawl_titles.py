import asyncio
import json
from datetime import datetime, timezone
from crawl4ai import AsyncWebCrawler

URLS_FILE = "discovered_urls.json"
OUTPUT_FILE = "raw_pages.jsonl"


async def crawl_title_pages():
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        title_urls = json.load(f)

    async with AsyncWebCrawler(verbose=True) as crawler:
        for url in title_urls:
            try:
                result = await crawler.arun(url=url, bypass_cache=True)

                record = {
                    "url": url,
                    "content": result.markdown,
                    "html": result.html,
                    "retrieved_at": datetime.now(timezone.utc).isoformat()
                }

                with open(OUTPUT_FILE, "a", encoding="utf-8") as out:
                    out.write(json.dumps(record) + "\n")

                print(f"[OK] Crawled title page: {url}")

            except Exception as e:
                print(f"[ERROR] Failed to crawl {url}: {e}")


if __name__ == "__main__":
    asyncio.run(crawl_title_pages())
