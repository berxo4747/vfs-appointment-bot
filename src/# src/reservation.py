# src/reservation.py

from playwright.sync_api import Page
from config_loader import load_settings

settings = load_settings()

def reserve_slot(page: Page, slot: dict):
    print(f"[INFO] Rezervasyon denemesi: {slot['date']} {slot['time']}")

    try:
        # Slot'a tıklama (selector örnek)
        slot_selector = f"button[data-date='{slot['date']}'][data-time='{slot['time']}']"
        page.click(slot_selector)
        page.wait_for_load_state("networkidle")

        # Form doldurma (örnek alanlar)
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
            print("[SUCCESS] Rezervasyon tamamlandı.")
            return True
        else:
            print("[ERROR] Rezervasyon başarısız.")
            return False

    except Exception as e:
        print(f"[ERROR] Rezervasyon sırasında hata oluştu: {e}")
        return False
