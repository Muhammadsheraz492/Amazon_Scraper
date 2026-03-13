import json
import asyncio
from playwright.async_api import async_playwright
import re
import json5
from scraper_modules.get_title import get_title
from scraper_modules.get_product_images import get_product_images
from scraper_modules.get_product_sizes import get_product_sizes
from scraper_modules.get_product_details import get_product_details
from scraper_modules.get_bullets import get_bullets
from scraper_modules.get_current_price import get_current_price
from scraper_modules.get_list_price import get_list_price
from scraper_modules.get_availability import get_availability
from scraper_modules.get_product_colors import get_product_colors
from scraper_modules.get_variants import get_variants

ZENROWS_API_KEY = "38b831b6d46b6fc43ff6d8d6697f5022c685939f"
CONNECTION_URL = f"wss://browser.zenrows.com?apikey={ZENROWS_API_KEY}"
MAX_RETRIES = 3

def save_products(all_products):
    """✅ Save after every product so no data is lost on crash."""
    with open("amazon_products.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)

async def goto_with_retry(page, url, retries=MAX_RETRIES):
    """Navigate to a URL with retries on timeout."""
    for attempt in range(1, retries + 1):
        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            return response
        except Exception as e:
            print(f"  ⚠️ Attempt {attempt}/{retries} failed for {url}: {e}")
            if attempt == retries:
                print(f"  ❌ Giving up on {url}")
                return None
            await asyncio.sleep(3)

async def run_scraper(urls):
    all_products = []

    async with async_playwright() as p:

        browser = await p.chromium.connect_over_cdp(CONNECTION_URL)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        for url in urls:
            print("Scraping:", url)

            try:
                # page.goto(url)
                # colors = await get_product_colors(page)
                # print(colors)

                # response = await page.goto(url)
                response = await goto_with_retry(page, url)
                if response is None:
                    all_products.append(dict(link=url, status="Failed"))
                    save_products(all_products)  # ✅ save even on failure
                    continue
                if response and response.status == 404:
                    print("❌ Page not found (404), skipping...")
                    product = dict(link=url, status="Not Found")
                    all_products.append(product)
                    save_products(all_products)  # ✅ save even on 404
                    continue

                # await page.wait_for_selector('script[type="a-state"]')

                # script_content = await page.locator(
                #     'script[type="a-state"][data-a-state*="f2-fit-size-guide"]'
                # ).text_content()

                # if script_content:
                #     data = json.loads(script_content.strip())
                #     asin = data.get("asin")
                    # print("ASIN:", asin)

                image_urls = await get_product_images(page)

                product = dict(
                    link=url,
                    current_price=await get_current_price(page),
                    list_price=await get_list_price(page),
                    availability=await get_availability(page),
                    title=await get_title(page),
                    image_urls=image_urls,
                    status="Scraped"
                )

                canonical = await page.locator('link[rel="canonical"]').get_attribute("href")
                match = re.search(r'/dp/([A-Z0-9]{10})', canonical)
                if match:
                    asin = match.group(1)
                    product["asin"] = asin
                    # print("ASIN:", asin)

                # print("Canonical URL:", canonical)

                product_data = await get_product_details(page)
                bullet_texts = await get_bullets(page)

                try:
                    variant_keys, formatted_variants = await get_variants(page=page, context=context)
                    if variant_keys and formatted_variants:
                        product["variant_keys"] = variant_keys
                        product["variants"] = formatted_variants
                except Exception as e:
                    print(f"  ⚠️ Variants failed for {url}: {e}")
                    # ✅ variants failed but product data is still saved below

                product['product_data'] = product_data
                product['bullet_texts'] = bullet_texts

                # scripts = page.locator("script")

                # count = await scripts.count()

                # for i in range(count):
                #     text = await scripts.nth(i).text_content()
                #     if text and "twister-js-init-dpx-data" in text:
                #         match = re.search(r'var\s+dataToReturn\s*=\s*({[\s\S]*?})\s*;', text)
                #         if not match:
                #             print("dataToReturn not found")
                #             exit()
                #         json_text = match.group(1)
                #         json_text = re.sub(r'"\s*\+\s*"', '', json_text)
                #         json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
                #         json_text = json_text.replace("\n", " ")
                #         data = json5.loads(json_text)

                #         print("Parsed successfully")
                #         print(data["dimensions"])
                #         print(data["dimensionValuesDisplayData"])
                #         variant_keys = data["dimensions"]
                #         variants_raw = data["dimensionValuesDisplayData"]

                #         formatted_variants = {}

                #         for variant_asin, values in variants_raw.items():
                #             variant_data = dict(zip(variant_keys, values))
                #             variant_url = f"https://www.amazon.com/dp/{variant_asin}"

                #             try:
                #                 await page.goto(variant_url, wait_until="domcontentloaded", timeout=30000)
                #                 await page.wait_for_timeout(2000)

                #                 variant_price = await get_current_price(page)
                #                 variant_list_price = await get_list_price(page)

                #                 print(f"  {variant_asin} -> {variant_price}")

                #             except Exception as e:
                #                 print(f"  Failed to scrape {variant_asin}: {e}")
                #                 variant_price = None
                #                 variant_list_price = None

                #             variant_data["current_price"] = variant_price
                #             variant_data["list_price"] = variant_list_price

                #             formatted_variants[variant_asin] = variant_data

                #         product["variant_keys"] = variant_keys
                #         product["variants"] = formatted_variants
                #         # with open("amazontesting_raw2.txt", "w", encoding="utf-8") as f:
                #         #     f.write(text)

                # input("Waiting")

                # sizes = await get_product_sizes(page)

                # excel_data = {
                #     "Url": url,
                #     "Title": title,
                #     "Images": image_urls,
                #     "Sizes": sizes,
                #     "About_Item": bullet_texts,
                #     "current_price": current_price,
                #     "Availability": availability,
                #     "list_price": list_price
                # }
                # for k, v in product_data.items():
                #     excel_data[k] = v

            except Exception as e:
                # ✅ Any unexpected crash — save what we have and move on
                print(f"  💥 Unexpected error scraping {url}: {e}")
                product = dict(link=url, status=f"Error: {str(e)}")

            all_products.append(product)
            save_products(all_products)  # ✅ save after every single product
            print(f"✅ Done: {product.get('title', url)} — total saved: {len(all_products)}\n")

        await browser.close()

    print("✅ All done! Saved all products!")