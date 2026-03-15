import gspread
from google.oauth2.service_account import Credentials
import json

def upload_to_sheet(all_products, service_account_file="credentials.json", spreadsheet_name="Amazon Products"):
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

    # --- Sheet Setup Function ---
    def setup_sheet(title, headers, col_widths=None):
        try:
            sheet = sh.worksheet(title)
            sheet.clear()
        except gspread.WorksheetNotFound:
            sheet = sh.add_worksheet(title=title, rows="1000", cols=str(len(headers)))
        sheet.append_row(headers)

        # Set column widths using batch_update
        if col_widths:
            requests = []
            for i, width in enumerate(col_widths):
                requests.append({
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": sheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": i,
                            "endIndex": i + 1
                        },
                        "properties": {"pixelSize": width},
                        "fields": "pixelSize"
                    }
                })
            sh.batch_update({"requests": requests})

        return sheet

    # --- Sheets ---
    products_sheet = setup_sheet(
        "Products",
        ["ASIN", "Title", "Brand", "Room Type", "Shape",
         "Product Dimensions", "Frame Material", "Link",
         "Current Price", "List Price", "Availability", "Status"],
        col_widths=[120, 300, 150, 200, 150, 180, 150, 250, 100, 100, 120, 100]
    )

    variants_sheet = setup_sheet(
        "Variants",
        ["Variant ASIN", "Parent ASIN", "Color", "Size", "Price"],
        col_widths=[150, 150, 150, 180, 100]
    )

    images_sheet = setup_sheet(
        "Images",
        ["Parent ASIN", "Image URL"],
        col_widths=[150, 300]
    )

    bullets_sheet = setup_sheet(
        "Bullet Points",
        ["Parent ASIN", "Bullet Point"],
        col_widths=[150, 400]
    )

    # --- Populate sheets ---
    for product in all_products:
        # Products
        products_sheet.append_row([
            product.get("asin"),
            product.get("title"),
            product.get("product_data", {}).get("Brand", ""),
            product.get("product_data", {}).get("Room Type", ""),
            product.get("product_data", {}).get("Shape", ""),
            product.get("product_data", {}).get("Product Dimensions", ""),
            product.get("product_data", {}).get("Frame Material", ""),
            product.get("link", ""),
            product.get("current_price", ""),
            product.get("list_price", ""),
            product.get("availability", ""),
            product.get("status", "")
        ])
        # Variants
        for var_asin, variant in product.get("variants", {}).items():
            variants_sheet.append_row([
                var_asin,
                product.get("asin"),
                variant.get("color_name", ""),
                variant.get("size_name", ""),
                variant.get("current_price", "")
            ])
        # Images
        for img_url in product.get("image_urls", []):
            images_sheet.append_row([product.get("asin"), img_url])
        # Bullets
        for bullet in product.get("bullet_texts", []):
            bullets_sheet.append_row([product.get("asin"), bullet])

    print(f"✅ Uploaded data to '{spreadsheet_name}' with 4 sheets and column widths set.")

