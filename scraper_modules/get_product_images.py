import re

def get_product_images(page):
    try:
        page.wait_for_selector("#altImages", timeout=5000)

        images = page.locator("#altImages li.imageThumbnail img")
        image_urls = []
        for i in range(images.count()):
            src = images.nth(i).get_attribute("src")
            if src and "play-button" not in src:
                image_urls.append(src)

        more_button = page.locator("#altImages li.overlayRestOfImages")
        if more_button.count() > 0:
            more_button.click()
            page.wait_for_selector("#ivThumbs", timeout=5000)
            thumbs = page.locator("#ivThumbs .ivThumbImage")
            for i in range(thumbs.count()):
                style_attr = thumbs.nth(i).get_attribute("style")
                if style_attr:
                    match = re.search(r'url\("([^"]+)"\)', style_attr)
                    if match:
                        url_highres = match.group(1).replace("_AC_US100_AA50_", "_AC_SL1500_")
                        image_urls.append(url_highres)

        return image_urls

    except Exception as e:
        print("Failed to get images:", e)
        return []