from playwright.sync_api import sync_playwright

EMAIL = "gustavo@murillotrust.com"
PASSWORD = "IrisPaloma2018!"

def amazon_login():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.amazon.com/")
        
        page.wait_for_selector('a[data-nav-role="signin"]')

        login_url = page.get_attribute('a[data-nav-role="signin"]', 'href')

        # print(login_url)
        page.goto(login_url)
        page.fill("#ap_email_login", EMAIL)
        page.click("#continue")
        page.wait_for_selector("#ap_password")
        page.fill("#ap_password", PASSWORD)
        page.click("#signInSubmit")
        print("Waiting for login...")
        # page.wait_for_load_state("networkidle")
        context.storage_state(path="amazon_login.json")
        print("Login session saved!")
        browser.close()