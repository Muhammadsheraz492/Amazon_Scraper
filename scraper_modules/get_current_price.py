def get_current_price(page):
    """
    Extracts the current price of the product.

    1. Try .priceToPay (symbol + whole + fraction)
    2. Fallback to .a-price .a-offscreen
    3. Return empty string if not found
    """

    try:
        price_block = page.locator(".priceToPay").first

        symbol = price_block.locator(".a-price-symbol").inner_text().strip()
        whole = price_block.locator(".a-price-whole").inner_text().strip().replace("\n", "")
        fraction = price_block.locator(".a-price-fraction").inner_text().strip()

        if whole and fraction:
            return f"{symbol}{whole}{fraction}"

    except Exception:
        pass

    # Fallback
    try:
        price = page.locator(".a-price .a-offscreen").first.inner_text().strip()
        return price
    except Exception:
        return ""