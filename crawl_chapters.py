import asyncio
import json
from datetime import datetime, timezone
from crawl4ai import AsyncWebCrawler

INPUT_FILE = "chapter_urls.json"
OUTPUT_FILE = "raw_chapter_pages.jsonl"

CONCURRENT_REQUESTS = 3   # keep low to avoid blocking
DELAY_BETWEEN_REQUESTS = 1  # seconds


async def crawl_one_chapter(crawler, chapter):
    url = chapter["chapter_url"]

    try:
        result = await crawler.arun(
            url=url,
            bypass_cache=True
        )

        record = {
            "url": url,
            "title_number": chapter.get("title_number"),
            "title_name": chapter.get("title_name"),
            "division_number": chapter.get("division_number"),
            "division_name": chapter.get("division_name"),
            "chapter_number": chapter.get("chapter_number"),
            "chapter_name": chapter.get("chapter_name"),
            "content": result.markdown,
            "html": result.html,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "success"
        }

        print(f"[OK] {url}")

    except Exception as e:
        record = {
            "url": url,
            "title_number": chapter.get("title_number"),
            "division_number": chapter.get("division_number"),
            "chapter_number": chapter.get("chapter_number"),
            "error": str(e),
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "status": "error"
        }

        print(f"[ERROR] {url}")

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)


async def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chapters = json.load(f)

    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    async with AsyncWebCrawler(verbose=True) as crawler:

        async def sem_task(chapter):
            async with semaphore:
                await crawl_one_chapter(crawler, chapter)

        await asyncio.gather(*(sem_task(ch) for ch in chapters))


if __name__ == "__main__":
    asyncio.run(main())