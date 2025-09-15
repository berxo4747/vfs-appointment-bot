# services/otp_fetcher.py

from services.email import get_latest_otp

def fetch_otp():
    """
    E-posta kutusundan en son gelen OTP kodunu çeker.
    """
    otp = get_latest_otp()
    if otp:
        print(f"[INFO] OTP başarıyla alındı: {otp}")
        return otp
    else:
        print("[WARN] OTP alınamadı.")
        return None
