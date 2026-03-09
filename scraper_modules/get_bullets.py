
def get_bullets(page):
    """
    Extract 'About This Item' bullet points.
    Returns a list of bullet strings.
    """
    bullets_list = []
    try:
        page.wait_for_selector("#feature-bullets ul", timeout=5000)
        bullets = page.locator("#feature-bullets ul li span.a-list-item")
        for i in range(bullets.count()):
            text = bullets.nth(i).inner_text().strip()
            if text:
                bullets_list.append(text)
        return bullets_list
    except Exception as e:
        print("Failed to get bullets:", e)
        return []