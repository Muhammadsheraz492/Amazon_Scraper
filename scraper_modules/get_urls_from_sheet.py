import gspread
from google.oauth2.service_account import Credentials

def get_urls_from_sheet(service_account_file="credentials.json", spreadsheet_name="Amazon Products", url_column="A"):
    """
    Reads a column of URLs from a Google Sheet (skipping the header) and returns them as a list.
    
    Parameters:
        service_account_file (str): Path to your Google service account JSON.
        spreadsheet_name (str): Name of the Google Sheet.
        url_column (str): Column letter where URLs are stored (default "A").
        
    Returns:
        list of URLs (str)
    """
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    gc = gspread.authorize(credentials)

    sh = gc.open(spreadsheet_name)
    worksheet = sh.sheet1

    urls = worksheet.col_values(ord(url_column.upper()) - 64) 
    urls = [url.strip() for url in urls[1:] if url.strip()] 

    return urls