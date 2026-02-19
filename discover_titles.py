import asyncio
import json
from crawl4ai import AsyncWebCrawler
from urllib.parse import urljoin

START_URL = "https://govt.westlaw.com/calregs"
OUTPUT_FILE = "discovered_urls.json"


async def discover_title_urls():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url=START_URL, bypass_cache=True)

        title_urls = set()

        # Use extracted markdown to find title links
        for line in result.markdown.splitlines():
            if "Title" in line and "(" in line and ")" in line:
                if "http" in line:
                    start = line.find("(") + 1
                    end = line.find(")")
                    url = line[start:end]
                    full_url = urljoin(START_URL, url)
                    title_urls.add(full_url)

        # Save discovered URLs
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(title_urls), f, indent=2)

        print(f"[DONE] Discovered {len(title_urls)} title URLs")


if __name__ == "__main__":
    asyncio.run(discover_title_urls())
