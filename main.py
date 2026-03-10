import os
from login import amazon_login
from scraper import run_scraper

LOGIN_FILE = "amazon_login.json"

if not os.path.exists(LOGIN_FILE):
    print("Login session not found. Running login script...")
    amazon_login()
else:
    print("Login session found.")

urls = [
    # "https://www.amazon.com/dp/B07PGL2ZSL",
    "https://a.co/d/0223Wvxd",
    # "https://www.amazon.com/dp/B07FZ8S74R"
]

run_scraper(urls)