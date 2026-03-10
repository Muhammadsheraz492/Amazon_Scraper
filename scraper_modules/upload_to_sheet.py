import gspread
from google.oauth2.service_account import Credentials
import json

def upload_to_sheet(all_products, service_account_file="credentials.json", spreadsheet_name="Amazon Products"):
    """
    Uploads a list of product dictionaries to a Google Sheet, converting list fields into strings.
    """
    if not all_products:
        print("No data to upload.")
        return

    # Load credentials
    with open(service_account_file, "r") as f:
        creds_dict = json.load(f)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    gc = gspread.authorize(credentials)

    # Open or create spreadsheet
    try:
        sh = gc.open(spreadsheet_name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(spreadsheet_name)
        sh.share(creds_dict["client_email"], perm_type="user", role="writer")

    worksheet = sh.sheet1

    # Prepare headers
    headers = list(all_products[0].keys())
    worksheet.clear()
    worksheet.append_row(headers)

    # Helper function to flatten list fields
    def flatten_value(value):
        if isinstance(value, list):
            if all(isinstance(i, dict) for i in value):
                return ", ".join([f"{d.get('size','')}:{d.get('price','')}" for d in value])
            else:
                # Remove duplicates in list of strings
                unique_items = list(dict.fromkeys(value))  # preserves order
                return ", ".join(unique_items)
        return value
    # Add rows
    for product in all_products:
        row = [flatten_value(product.get(h, "")) for h in headers]
        worksheet.append_row(row)

    print(f"✅ Uploaded {len(all_products)} products to Google Sheet '{spreadsheet_name}'")