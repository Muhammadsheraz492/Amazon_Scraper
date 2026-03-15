# scraper_modules/handle_captcha.py

async def handle_captcha(page):
    """Detect and handle Amazon CAPTCHA / Continue shopping page."""
    try:
        # ✅ Save HTML for debugging
        html = await page.content()
        with open("captcha_page.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("💾 HTML saved to captcha_page.html")

        continue_btn = page.locator('button.a-button-text[alt="Continue shopping"]')

        if await continue_btn.count() > 0:
            try:
                await continue_btn.click()
                print("🛒 Clicked 'Continue shopping' button")

                # ✅ Wait a little
                await page.wait_for_timeout(2000)

                # ✅ Reload page
                await page.reload()

                # ✅ Wait for product page
                await page.wait_for_selector("#productTitle", timeout=10000)

                print("✅ Passed CAPTCHA page")
                return True

            except Exception as e:
                print(f"❌ Click failed: {e}")

                # fallback reload
                await page.reload()
                return False

    except Exception as e:
        print(f"⚠️ CAPTCHA handle failed: {e}")

    return False