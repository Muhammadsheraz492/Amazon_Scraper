
def get_list_price(page):

    try:
        list_price = page.locator(".basisPrice .a-offscreen").first.inner_text().strip()
        return list_price
    except Exception as e:
        # print("Failed to get list price:", e)
        return ""