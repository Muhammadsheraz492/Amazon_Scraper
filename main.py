import os
from login import amazon_login
from scraper import run_scraper
import json
from scraper_modules.upload_to_sheet import upload_to_sheet
from scraper_modules.get_urls_from_sheet import get_urls_from_sheet

urls = get_urls_from_sheet(
    service_account_file="credentials.json",
    spreadsheet_name="Amazon Products",
    url_column="A"  
)
print("URLs to scrape:", urls)

LOGIN_FILE = "amazon_login.json"

if not os.path.exists(LOGIN_FILE):
    print("Login session not found. Running login script...")
    amazon_login()
else:
    print("Login session found.")



run_scraper(urls)
with open("amazon_products.json", "r", encoding="utf-8") as f:
    all_products = json.load(f)

upload_to_sheet(
    all_products,
    service_account_file="credentials.json",  
    spreadsheet_name="Amazon Products"         
)