# src/appointment_checker.py

from playwright.sync_api import Page
from config_loader import load_settings

settings = load_settings()

def navigate_to_appointment_page(page: Page):
    print("[INFO] Randevu ekranına gidiliyor...")
    page.goto(settings["vfs"]["dashboard_url"])
    page.wait_for_load_state("networkidle")

def check_available_slots(page: Page):
    navigate_to_appointment_page(page)

    # Örnek selector — gerçek DOM'a göre güncellenmeli
    slot_elements = page.query_selector_all("div[class*='appointment-slot'], button[data-date]")

    preferred_dates = settings["appointment"]["preferred_dates"]
    preferred_times = settings["appointment"]["preferred_times"]

    available = []

    for slot in slot_elements:
        date = slot.get_attribute("data-date")
        time_ = slot.get_attribute("data-time")

        if not date or not time_:
            continue

        if date in preferred_dates and time_ in preferred_times:
            available.append({"date": date, "time": time_})
            print(f"[MATCH] Uygun slot bulundu: {date} {time_}")

    if not available:
        print("[INFO] Uygun randevu bulunamadı.")
    return available
