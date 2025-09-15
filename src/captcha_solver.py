# src/captcha_solver.py

from playwright.sync_api import Page

def solve_cloudflare_captcha(page: Page):
    print("[INFO] Cloudflare CAPTCHA çözümü başlatılıyor...")

    try:
        # CAPTCHA iframe'ini bekle
        iframe_element = page.wait_for_selector("iframe[title*='Cloudflare']", timeout=15000)
        captcha_frame = iframe_element.content_frame()

        # Checkbox'ı bul ve tıkla
        checkbox = captcha_frame.wait_for_selector("input[type='checkbox']", timeout=10000)
        checkbox.click()
        print("[SUCCESS] CAPTCHA checkbox tıklandı.")

        # CAPTCHA çözümünü bekle
        page.wait_for_load_state("networkidle")
        print("[INFO] CAPTCHA çözümü tamamlandı.")
        return True
    except Exception as e:
        print(f"[ERROR] CAPTCHA çözümü başarısız: {e}")
        return False
def test_cloudflare_captcha():
    from playwright.sync_api import sync_playwright
    from src.captcha_solver import solve_cloudflare_captcha

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://visa.vfsglobal.com/tur/tr/nld/application-detail")
        result = solve_cloudflare_captcha(page)
        assert result is True
        browser.close()
