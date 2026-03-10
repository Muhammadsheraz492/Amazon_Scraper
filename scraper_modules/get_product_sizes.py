from .get_current_price import get_current_price

def get_product_sizes(page):
    """
    Clicks each available size and returns its price
    """

    results = []

    try:
        page.wait_for_selector("#tp-inline-twister-dim-values-container", timeout=5000)

        sizes = page.locator("#tp-inline-twister-dim-values-container li.swatch-list-item-text")
        count = sizes.count()

        for i in range(count):
            try:
                size_item = sizes.nth(i)

                # Skip unavailable sizes
                class_attr = size_item.get_attribute("class") or ""
                if "a-button-unavailable" in class_attr:
                    continue

                size_text = size_item.locator(".swatch-title-text-display").inner_text().strip()

                # Click the button inside
                button = size_item.locator("input.a-button-input")
                button.scroll_into_view_if_needed()
                button.click()
                price = get_current_price(page)
                results.append({
                    "size": size_text,
                    "price": price
                })

            except Exception as size_error:
                print(f"Error processing size index {i}: {size_error}")
                continue

    except Exception as e:
        print("Error getting sizes and prices:", e)

    return results