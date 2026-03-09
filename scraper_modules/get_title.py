def get_title(page):
    try:
        page.wait_for_selector("#productTitle", timeout=5000)
        title = page.locator("span#productTitle").inner_text().strip()
        return title
    except Exception:
        return "Unknown Product"