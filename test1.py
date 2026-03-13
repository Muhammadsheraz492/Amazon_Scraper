import json

from playwright.sync_api import sync_playwright
import re
import json5
from scraper_modules.get_title import get_title;
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
def goto_with_retry(page, url, retries=MAX_RETRIES):
    """Navigate to a URL with retries on timeout."""
    for attempt in range(1, retries + 1):
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            return response
        except Exception as e:
            print(f"  ⚠️ Attempt {attempt}/{retries} failed for {url}: {e}")
            if attempt == retries:
                print(f"  ❌ Giving up on {url}")
                return None
            page.wait_for_timeout(3000) 
            
async def run_scraper(urls):
    all_products = []
   async with sync_playwright() as p:

        browser = await p.chromium.connect_over_cdp(CONNECTION_URL)
        context = browser.contexts[0] if browser.contexts else await browser.new_context()
        page = await context.new_page()

        for url in urls:

            print("Scraping:", url)
            page.goto(url)
            # colors = get_product_colors(page)

            # print(colors)
            
            # response = page.goto(url)
            response = goto_with_retry(page, url)
            if response is None:
                all_products.append(dict(link=url, status="Failed"))
                continue
            if response and response.status == 404:
                print("❌ Page not found (404), skipping...")
                product = dict(
                    link=url,
                    status="Not Found"
                )
                all_products.append(product)
                continue
            # page.wait_for_selector('script[type="a-state"]')

            # script_content = page.locator(
            #     'script[type="a-state"][data-a-state*="f2-fit-size-guide"]'
            # ).text_content()

            # if script_content:
            #     data = json.loads(script_content.strip())
            #     asin = data.get("asin")
                # print("ASIN:", asin)
            image_urls = get_product_images(page)
                
            product = dict(
                link=url,
                current_price=get_current_price(page),
                list_price=get_list_price(page),
                availability=get_availability(page),
                title=get_title(page),
                image_urls=image_urls,
                status="Scraped"
            )
                            
      
            canonical = page.locator('link[rel="canonical"]').get_attribute("href")
            match = re.search(r'/dp/([A-Z0-9]{10})', canonical)

            if match:
                asin = match.group(1)
                product["asin"] = asin
                # print("ASIN:", asin)
            
            product_data = get_product_details(page)
            bullet_texts = get_bullets(page)
            variant_keys, formatted_variants = get_variants(page)

            if variant_keys and formatted_variants:
                product["variant_keys"] = variant_keys
                product["variants"] = formatted_variants

            
            # print("Canonical URL:", canonical)

            # scripts = page.locator("script")

            # count = scripts.count()

            # for i in range(count):
            #     text = scripts.nth(i).text_content()
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
            #                 page.goto(variant_url, wait_until="domcontentloaded", timeout=30000)
            #                 page.wait_for_timeout(2000) 
                            
            #                 variant_price = get_current_price(page)
            #                 variant_list_price = get_list_price(page)
                            
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
           
            # sizes = get_product_sizes(page)
            
          
           
            # excel_data = {
            #     "Url":url,
            #     "Title": title,
            #     "Images": image_urls,
            #     "Sizes": sizes,
            #     "About_Item": bullet_texts,
            #     "current_price":current_price,
            #     "Availability":availability,
            #     "list_price":list_price
            # }
            # for k, v in product_data.items():
            #     excel_data[k] = v

            all_products.append(product)

        browser.close()

    with open("amazon_products.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
    print("Saved all products!")