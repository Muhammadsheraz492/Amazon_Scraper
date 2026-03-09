
def get_current_price(page):
    """
    Extracts the current price of the product.
    1. Try .priceToPay (whole + fraction)
    2. Fallback to .a-text-price .a-offscreen
    Returns a string like "$32.99". If not found, returns empty string.
    """

    try:
        whole_locator = page.locator(".priceToPay .a-price-whole")
        fraction_locator = page.locator(".priceToPay .a-price-fraction")

        if whole_locator.count() > 0 and fraction_locator.count() > 0:
            whole = whole_locator.first.inner_text().strip().replace("\n", "")
            fraction = fraction_locator.first.inner_text().strip()
            return f"${whole}{fraction}"

    except Exception:
        pass

    # Fallback price
    try:
        price = page.locator(".a-text-price .a-offscreen").first.inner_text().strip()
        return price
    except Exception as e:
        # print("Failed to get current price:", e)
        return ""