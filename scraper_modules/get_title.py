async def get_title(page):
    try:
        await page.wait_for_selector("#productTitle", timeout=5000)
        title = (await page.locator("span#productTitle").inner_text()).strip()
        return title
    except Exception:
        return "Unknown Product"