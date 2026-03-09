# components/get_price.py

def get_current_price(page):
    """
    Extracts the current price of the product from the page.
    Returns a string like "$32.99". If not found, returns empty string.
    """
    try:
        whole = page.locator(".priceToPay .a-price-whole").first.inner_text().strip().replace("\n","")
        fraction = page.locator(".priceToPay .a-price-fraction").first.inner_text().strip()
        return f"${whole}{fraction}"
    except Exception as e:
        print("Failed to get current price:", e)
        return ""