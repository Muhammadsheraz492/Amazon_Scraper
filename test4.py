import json
import asyncio
from playwright.async_api import async_playwright
from scraper_modules.get_current_price  import get_current_price;

CONNECTION_URL = "wss://browser.zenrows.com?apikey=38b831b6d46b6fc43ff6d8d6697f5022c685939f&proxy_country=us"

async def main():
    with open("amazon_products.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    async with async_playwright() as p:
        for itm in data:
            variants = itm.get("variants", {})
            for key in variants:
                browser = await p.chromium.connect_over_cdp(CONNECTION_URL)
                variant_url = f"https://www.amazon.com/dp/{key}"
                print("Opening:", variant_url)
                if browser.contexts:
                    context = browser.contexts[0]
                else:
                    context = await browser.new_context(ignore_https_errors=True)
                page = await context.new_page()
                await page.goto(variant_url, wait_until="domcontentloaded")
                try:
                    price = await get_current_price(page)
                    variants[key]["current_price"] = price
                    print("Title:", price)
                except:
                    print("⚠️ Could not find product title")
                await page.close()
                await browser.close()

asyncio.run(main())