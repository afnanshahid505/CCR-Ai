import asyncio
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler

START_URL = "https://govt.westlaw.com/calregs"
OUTPUT_FILE = "raw_pages.jsonl"


async def crawl_ccr():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=START_URL,
            bypass_cache=True
        )

        record = {
            "url": START_URL,
            "content": result.markdown,   # extracted content
            "html": result.html,          # raw html
            "retrieved_at": datetime.utcnow().isoformat()
        }

        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        print("[DONE] Page crawled and stored")


if __name__ == "__main__":
    asyncio.run(crawl_ccr())
