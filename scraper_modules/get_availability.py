
def get_availability(page):
    """
    Extract product availability (e.g., 'In Stock').
    Returns a string. If not found, returns empty string.
    """
    try:
        availability = page.locator("#availability span").inner_text().strip()
        return availability
    except Exception as e:
        # print("Failed to get availability:", e)
        return ""