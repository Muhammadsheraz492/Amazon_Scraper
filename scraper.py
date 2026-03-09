from playwright.sync_api import sync_playwright
import re
import json
from scraper_modules.get_title import get_title;
from scraper_modules.get_product_images import get_product_images
from scraper_modules.get_product_sizes import get_product_sizes
from scraper_modules.get_product_details import get_product_details
from scraper_modules.get_bullets import get_bullets
from scraper_modules.get_current_price import get_current_price
from scraper_modules.get_list_price import get_list_price
from scraper_modules.get_availability import get_availability
def run_scraper(urls):

    all_products = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="amazon_login.json")
        page = context.new_page()

        for url in urls:

            print("Scraping:", url)
            page.goto(url)
            title = get_title(page)
            image_urls = get_product_images(page)
            sizes = get_product_sizes(page)
            current_price = get_current_price(page)            
            list_price = get_list_price(page)
            availability = get_availability(page)
            product_data = get_product_details(page)
            bullet_texts = get_bullets(page)
            excel_data = {
                "Url":url,
                "Title": title,
                "Images": image_urls,
                "Sizes": sizes,
                "About_Item": bullet_texts,
                "current_price":current_price,
                "Availability":availability,
                "list_price":list_price
            }
            for k, v in product_data.items():
                excel_data[k] = v

            all_products.append(excel_data)

        browser.close()

    with open("amazon_products.json", "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
    input("Testing")
    print("Saved all products!")