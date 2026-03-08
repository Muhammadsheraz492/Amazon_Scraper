from playwright.sync_api import sync_playwright
import pandas as pd # type: ignore
import re
url = "https://a.co/d/0223Wvxd"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_selector("#productTitle")
    title = page.locator("span#productTitle").inner_text().strip()
    print("Product Title:",title);
    page.wait_for_selector("#altImages")
    # html = page.locator("#altImages").inner_html()
    images = page.locator("#altImages li.imageThumbnail img")
    count = images.count()
    image_urls = []
    for i in range(count):
        src = images.nth(i).get_attribute("src")
        if src and "play-button" not in src:
            image_urls.append(src)
    more_button = page.locator("#altImages li.overlayRestOfImages")
    image_urls = []
    if more_button.count() > 0:
        more_button.click()
        page.wait_for_selector("#ivThumbs")
        thumbs = page.locator("#ivThumbs .ivThumbImage")
        for i in range(thumbs.count()):
            style_attr = thumbs.nth(i).get_attribute("style")
            if style_attr:
                match = re.search(r'url\("([^"]+)"\)', style_attr)
                if match:
                    url_highres = match.group(1).replace("_AC_US100_AA50_", "_AC_SL1500_")
                    image_urls.append(url_highres)
    for img in image_urls:
        print(img)
        
    page.wait_for_selector("#tp-inline-twister-dim-values-container")

    size_elements = page.locator(
        "#tp-inline-twister-dim-values-container li.swatch-list-item-text .swatch-title-text-display"
    )
    sizes = [size_elements.nth(i).inner_text().strip() for i in range(size_elements.count())]

    print("Available Sizes:",len(sizes))
    for s in sizes:
        print(s)
    page.wait_for_selector(".po-brand")

    rows = page.locator("table.a-normal tr")

    data = {}

    for i in range(rows.count()):
        row = rows.nth(i)

        key = row.locator("td").nth(0).inner_text().strip()
        value = row.locator("td").nth(1).inner_text().strip()

        data[key] = value

    print("\nProduct Details:\n")

    for k, v in data.items():
        print(f"{k}: {v}")
    page.wait_for_selector("#feature-bullets ul")

    bullets = page.locator("#feature-bullets ul li span.a-list-item")
    bullet_texts = [bullets.nth(i).inner_text().strip() for i in range(bullets.count())]

    print("\nAbout This Item:\n")
    for b in bullet_texts:
        print("-", b)
    
    excel_data = {
        "Title": title,
        "Images": ", ".join(image_urls),
        "Sizes": ", ".join(sizes),
        "About Item": " | ".join(bullet_texts)
    }
    for k, v in data.items():
        excel_data[k] = v

    df = pd.DataFrame([excel_data])

    df.to_excel("amazon_product.xlsx", index=False)

    print("Data saved to amazon_product.xlsx")
    browser.close()