# components/get_product_details.py

async def get_product_details(page):
    """
    Extract product specifications/details from the table.
    Returns a dictionary of key-value pairs.
    """
    data = {}
    try:
        await page.wait_for_selector(".po-brand", timeout=5000)
        rows = page.locator("table.a-normal tr")
        for i in range(await rows.count()):
            row = rows.nth(i)
            key = (await row.locator("td").nth(0).inner_text()).strip()
            value = (await row.locator("td").nth(1).inner_text()).strip()
            if key or value:  # skip empty rows
                data[key] = value
        return data
    except Exception as e:
        # print("Failed to get product details:", e)
        return {}