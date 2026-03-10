from .get_current_price import get_current_price

def get_product_colors(page):

    results = []

    try:
        page.wait_for_selector("#tp-inline-twister-dim-values-container")

        if page.locator("#cx-expander").count() > 0:
            page.locator("#cx-expander").click()

        colors = page.locator(
            "#tp-inline-twister-dim-values-container li.dimension-value-list-item-square-image"
        )

        count = colors.count()

        for i in range(count):

            try:
                color_item = colors.nth(i)

                # skip hidden
                style = color_item.get_attribute("style") or ""
                if "display: none" in style:
                    continue

                # skip unavailable
                if color_item.locator(".a-button-unavailable").count() > 0:
                    continue

                img = color_item.locator("img.swatch-image").first

                if img.count() == 0:
                    continue

                color_name = img.get_attribute("alt")

                button = color_item.locator("input.a-button-input").first

                button.scroll_into_view_if_needed()
                button.click()

                page.wait_for_timeout(1500)

                price = get_current_price(page)

                results.append({
                    "color": color_name,
                    "price": price
                })

            except Exception as e:
                print(f"Error processing color {i}:", e)

        return results

    except Exception as e:
        print("Color scraping error:", e)
        return []