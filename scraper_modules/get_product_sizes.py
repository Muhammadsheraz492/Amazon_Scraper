
def get_product_sizes(page):
    try:
        page.wait_for_selector("#tp-inline-twister-dim-values-container", timeout=5000)

        size_elements = page.locator(
            "#tp-inline-twister-dim-values-container li.swatch-list-item-text .swatch-title-text-display"
        )
        sizes = [size_elements.nth(i).inner_text().strip() for i in range(size_elements.count())]

        return sizes

    except Exception as e:
        # print("Failed to get sizes:", e)
        return []