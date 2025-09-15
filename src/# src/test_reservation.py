# src/reservation.py

from playwright.sync_api import Page
from config_loader import load_settings

settings = load_settings()

# Desteklenen lokasyonlar
SUPPORTED_LOCATIONS = [
    "Netherlands Visa Application Centre - Ankara",
    "Netherlands Visa Application Centre - Bursa",
    "Netherlands Visa Application Centre - ALTUNIZADE",
    "Netherlands Visa Application Centre - BEYOGLU"
]

def select_location(page: Page):
    print("[INFO] Lokasyon seçimi yapılıyor...")
    location_elements = page.query_selector_all("span.mdc-list-item__primary-text")

    for element in location_elements:
        location_text = element.inner_text().strip()
        if location_text in SUPPORTED_LOCATIONS:
            print(f"[MATCH] Lokasyon bulundu: {location_text}")
            element.click()
            page.wait_for_load_state("networkidle")
            return location_text

    raise Exception("[ERROR] Uygun lokasyon bulunamadı.")

def reserve_slot(page: Page, slot: dict):
    print(f"[INFO] Rezervasyon denemesi: {slot['date']} {slot['time']}")

    try:
        # Lokasyon seçimi
        selected_location = select_location(page)

        # Slot'a tıklama (örnek selector)
        slot_selector = f"button[data-date='{slot['date']}'][data-time='{slot['time']}']"
        page.click(slot_selector)
        page.wait_for_load_state("networkidle")

        # Form doldurma
        page.fill('input[name="firstName"]', "Merwan")
        page.fill('input[name="lastName"]', "Yılmaz")
        page.fill('input[name="passportNumber"]', "X1234567")
        page.fill('input[name="phone"]', "+905555555555")
        page.fill('input[name="email"]', settings["notification"]["email"]["recipient"])

        # Onay kutusu ve gönderim
        page.check('input[name="terms"]')
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")

        # Başarı kontrolü
        if "confirmation" in page.url or page.locator("text=Randevu başarıyla alındı").is_visible():
            print(f"[SUCCESS] Rezervasyon tamamlandı ({selected_location}).")
            return True
        else:
            print("[ERROR] Rezervasyon başarısız.")
            return False

    except Exception as e:
        print(f"[ERROR] Rezervasyon sırasında hata oluştu: {e}")
        return False
