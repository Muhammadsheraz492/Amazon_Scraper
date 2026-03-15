ZENROWS_API_KEY = "38b831b6d46b6fc43ff6d8d6697f5022c685939f"
CONNECTION_URL = f"wss://browser.zenrows.com?apikey={ZENROWS_API_KEY}&proxy_country=us"

import asyncio
from .handle_captcha import handle_captcha
from .get_current_price import get_current_price
from .get_title import get_title;
# Limit concurrency to 2 browsers at a time
semaphore = asyncio.Semaphore(2)

async def scrape_variant_price(p, key, variants):
    async with semaphore:
        browser = await p.chromium.connect_over_cdp(CONNECTION_URL)

        # Reuse context if it exists
        if browser.contexts:
            context = browser.contexts[0]
        else:
            context = await browser.new_context(ignore_https_errors=True)

        page = await context.new_page()
        variant_url = f"https://www.amazon.com/dp/{key}"
        print("Opening:", variant_url)

        try:
            await page.goto(variant_url, wait_until="domcontentloaded")

            # Handle CAPTCHA if any
            captcha_solved = await handle_captcha(page)
            if captcha_solved:
                print("CAPTCHA handled successfully")
            else:
                print("No CAPTCHA detected or handling failed")
                title=await get_title(page)
                if title:
                    print("Product Available");
                else:
                    print("No CAPTCHA or handling failed")
                    return;

            # Scrape price
            price = await get_current_price(page)
            variants[key]["current_price"] = price
            print(f"Variant {key} price: {price}")

        except Exception as e:
            print(f"⚠️ Could not scrape variant {key}: {e}")

        finally:
            await page.close()
            await browser.close()