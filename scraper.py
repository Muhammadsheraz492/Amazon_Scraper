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
            # page.wait_for_selector("#productTitle")
            # title = page.locator("span#productTitle").inner_text().strip()
            # print("Product Title:",title);
            title = get_title(page)
            print("Product Title:", title)
            # page.wait_for_selector("#altImages")
            # # html = page.locator("#altImages").inner_html()
            # images = page.locator("#altImages li.imageThumbnail img")
            # count = images.count()
            # image_urls = []
            # for i in range(count):
            #     src = images.nth(i).get_attribute("src")
            #     if src and "play-button" not in src:
            #         image_urls.append(src)
            # more_button = page.locator("#altImages li.overlayRestOfImages")
            # image_urls = []
            # if more_button.count() > 0:
            #     more_button.click()
            #     page.wait_for_selector("#ivThumbs")
            #     thumbs = page.locator("#ivThumbs .ivThumbImage")
            #     for i in range(thumbs.count()):
            #         style_attr = thumbs.nth(i).get_attribute("style")
            #         if style_attr:
            #             match = re.search(r'url\("([^"]+)"\)', style_attr)
            #             if match:
            #                 url_highres = match.group(1).replace("_AC_US100_AA50_", "_AC_SL1500_")
            #                 image_urls.append(url_highres)
            # for img in image_urls:
            #     print(img)
            
            image_urls = get_product_images(page)
                
            # page.wait_for_selector("#tp-inline-twister-dim-values-container")

            # size_elements = page.locator(
            #     "#tp-inline-twister-dim-values-container li.swatch-list-item-text .swatch-title-text-display"
            # )
            # sizes = [size_elements.nth(i).inner_text().strip() for i in range(size_elements.count())]
            sizes = get_product_sizes(page)
            # current_price = page.locator(".priceToPay .a-offscreen").first.inner_text().strip() 
            # whole = page.locator(".priceToPay .a-price-whole").first.inner_text().strip().replace("\n","") 
            # fraction = page.locator(".priceToPay .a-price-fraction").first.inner_text().strip() 
            # current_price = f"${whole}{fraction}" 
            current_price = get_current_price(page)
            print("Current Price:", current_price)
            # list_price = page.locator(".basisPrice .a-offscreen").first.inner_text().strip()
            # availability = page.locator("#availability span").inner_text().strip() 
            
            list_price = get_list_price(page)
            availability = get_availability(page)

            print("Available Sizes:",len(sizes))
            # page.wait_for_selector(".po-brand")

            # rows = page.locator("table.a-normal tr")

            # data = {}

            # for i in range(rows.count()):
            #     row = rows.nth(i)

            #     key = row.locator("td").nth(0).inner_text().strip()
            #     value = row.locator("td").nth(1).inner_text().strip()

            #     data[key] = value
            product_data = get_product_details(page)
            
            # page.wait_for_selector("#feature-bullets ul")

            # bullets = page.locator("#feature-bullets ul li span.a-list-item")
            # bullet_texts = [bullets.nth(i).inner_text().strip() for i in range(bullets.count())]
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

    print("Saved all products!")