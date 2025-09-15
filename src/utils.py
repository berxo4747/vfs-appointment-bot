# src/utils.py

import time
import functools

def retry(max_attempts=3, delay=5):
    """
    Fonksiyonu belirli sayıda tekrar denemek için dekoratör.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[WARN] Deneme {attempt}/{max_attempts} başarısız: {e}")
                    time.sleep(delay)
            raise Exception(f"[FAIL] {func.__name__} başarısız oldu.")
        return wrapper
    return decorator

def format_slot(slot: dict) -> str:
    """
    Slot sözlüğünü okunabilir metne çevirir.
    """
    return f"{slot.get('date', '??')} - {slot.get('time', '??')}"
