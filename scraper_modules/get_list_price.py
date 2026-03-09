
def get_list_price(page):
    """
    Extracts the list/original price of the product.
    Returns a string like "$39.99". If not found, returns empty string.
    """
    try:
        list_price = page.locator(".basisPrice .a-offscreen").first.inner_text().strip()
        return list_price
    except Exception as e:
        # print("Failed to get list price:", e)
        return ""