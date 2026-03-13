# scraper_modules/get_variants.py

import re
import json5
import asyncio
from scraper_modules.get_current_price import get_current_price
from scraper_modules.get_list_price import get_list_price

async def get_variants(page, context):
    scripts = page.locator("script")
    count = await scripts.count()

    for i in range(count):
        try:
            text = await scripts.nth(i).text_content(timeout=3000)
        except Exception:
            continue

        if text and "twister-js-init-dpx-data" in text:
            match = re.search(r'var\s+dataToReturn\s*=\s*({[\s\S]*?})\s*;', text)
            if not match:
                print("dataToReturn not found")
                return None, None

            json_text = match.group(1)
            json_text = re.sub(r'"\s*\+\s*"', '', json_text)
            json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
            json_text = json_text.replace("\n", " ")

            try:
                data = json5.loads(json_text)
            except Exception as e:
                print(f"❌ Failed to parse twister JSON: {e}")
                return None, None

            print("Parsed successfully")
            print(data["dimensions"])
            print(data["dimensionValuesDisplayData"])

            variant_keys = data["dimensions"]
            variants_raw = data["dimensionValuesDisplayData"]
            formatted_variants = {}

            # ✅ Separate page so main page is never touched
            variant_page = await context.new_page()

            for variant_asin, values in variants_raw.items():
                variant_data = dict(zip(variant_keys, values))
                variant_url = f"https://www.amazon.com/dp/{variant_asin}"

                try:
                    await variant_page.goto(variant_url, wait_until="domcontentloaded", timeout=60000)
                    await asyncio.sleep(2)  # ✅ async sleep instead of wait_for_timeout

                    variant_data["current_price"] = await get_current_price(variant_page)
                    variant_data["list_price"] = await get_list_price(variant_page)

                    print(f"  ✅ {variant_asin} -> {variant_data['current_price']}")

                except Exception as e:
                    print(f"  ❌ Failed to scrape {variant_asin}: {e}")
                    variant_data["current_price"] = None
                    variant_data["list_price"] = None

                formatted_variants[variant_asin] = variant_data

            await variant_page.close()  # ✅ only closes variant_page, main page untouched
            return variant_keys, formatted_variants

    return None, None