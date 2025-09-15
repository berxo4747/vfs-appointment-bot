# services/email.py

import imaplib
import email
import re
from config_loader import load_settings

settings = load_settings()

def get_latest_otp():
    try:
        mail = imaplib.IMAP4_SSL(settings["otp"]["email_host"])
        mail.login(settings["otp"]["email_user"], settings["otp"]["email_pass"])
        mail.select("inbox")

        # Sadece VFS Global'dan gelen e-postaları filtrele
        result, data = mail.search(None, f'(FROM "{settings["otp"]["sender_filter"]}")')
        mail_ids = data[0].split()

        if not mail_ids:
            print("[INFO] OTP e-postası bulunamadı.")
            return None

        latest_email_id = mail_ids[-1]
        result, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        # E-posta içeriğini al
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        # OTP kodunu ayıkla (örnek: 6 haneli sayı)
        otp_match = re.search(r"\b\d{6}\b", body)
        if otp_match:
            otp = otp_match.group(0)
            print(f"[SUCCESS] OTP bulundu: {otp}")
            return otp
        else:
            print("[ERROR] OTP formatı bulunamadı.")
            return None

    except Exception as e:
        print(f"[ERROR] E-posta kontrolü sırasında hata: {e}")
        return None
