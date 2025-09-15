def test_slot_filtering():
    from playwright.sync_api import sync_playwright
    from src.appointment_checker import check_available_slots

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        slots = check_available_slots(page)
        assert isinstance(slots, list)
        browser.close()
