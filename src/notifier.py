# src/notifier.py

import requests
import smtplib
from email.mime.text import MIMEText
from config_loader import load_settings

settings = load_settings()

def send_telegram_message(message: str):
    if not settings["notification"]["telegram"]["enabled"]:
        return

    token = settings["notification"]["telegram"]["bot_token"]
    chat_id = settings["notification"]["telegram"]["chat_id"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("[SUCCESS] Telegram bildirimi gönderildi.")
        else:
            print(f"[ERROR] Telegram bildirimi başarısız: {response.text}")
    except Exception as e:
        print(f"[ERROR] Telegram gönderim hatası: {e}")

def send_email(subject: str, body: str):
    if not settings["notification"]["email"]["enabled"]:
        return

    smtp_host = settings["notification"]["email"]["smtp_host"]
    smtp_port = settings["notification"]["email"]["smtp_port"]
    sender = settings["notification"]["email"]["sender"]
    password = settings["notification"]["email"]["password"]
    recipient = settings["notification"]["email"]["recipient"]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        print("[SUCCESS] E-posta bildirimi gönderildi.")
    except Exception as e:
        print(f"[ERROR] E-posta gönderim hatası: {e}")
