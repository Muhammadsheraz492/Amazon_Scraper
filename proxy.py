import asyncio
from playwright.async_api import async_playwright

API_URL = "wss://browser.zenrows.com?apikey=38b831b6d46b6fc43ff6d8d6697f5022c685939f&proxy_country=us"

async def main():
    async with async_playwright() as p:

        for i in range(3):
            browser = await p.chromium.connect_over_cdp(API_URL)

            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://httpbin.org/ip")
            print(f"Request {i+1}: {await page.text_content('body')}")

            await browser.close()

asyncio.run(main())