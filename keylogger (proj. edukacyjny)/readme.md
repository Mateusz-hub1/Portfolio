# Keylogger z integracją Google Sheets (Python)

Ten projekt to keylogger napisany w Pythonie, umożliwiający rejestrowanie naciśnięć klawiszy i ich zapisywanie:
- lokalnie do pliku tekstowego (`keylog.txt`)
- zdalnie do arkusza Google Sheets

Obsługuje szyfrowanie danych (`Fernet`) oraz pełną konfigurację przez plik `.env`.

---

## 🧩 Funkcje

- Rejestruje znaki wpisywane z klawiatury w czasie rzeczywistym
- Flush co `N` znaków lub `X` sekund
- Obsługa znaków specjalnych (spacja, enter, tab)
- Zapisuje dane lokalnie (z opcjonalnym szyfrowaniem)
- Wysyła dane do wskazanego arkusza Google
- W pełni konfigurowalny przez `.env`

---

## ⚙️ Konfiguracja `.env`

Przykład pliku `.env`:

```dotenv
SERVICE_ACCOUNT_FILE=service_account.json
SPREADSHEET_ID=your_google_spreadsheet_id
WORKSHEET_NAME=Arkusz1

DURATION_S=60
FLUSH_EVERY_N_KEYS=10
FLUSH_EVERY_SEC=30

LOG_FILE=keylog.txt
```
# Do szyfrowania (opcjonalnie)
FERNET_KEY=b'ZAKODOWANY_KLUCZ_BASE64'

⸻

 Uruchomienie
1.	Zainstaluj zależności:
pip install -r requirements.txt
2.	Przygotuj plik .env na podstawie powyższego przykładu.
 
 3.	Uruchom:
		python keylogger.py



Po zakończeniu działania (DURATION_S) dane zostaną zapisane lokalnie i opcjonalnie przesłane do Google Sheets.

⸻

 Szyfrowanie

Aby włączyć szyfrowanie lokalnego pliku:
	1.	Wygeneruj klucz:

from cryptography.fernet import Fernet
print(Fernet.generate_key())


	2.	Wstaw go do .env jako FERNET_KEY.

⸻

 Zastrzeżenie

Projekt służy wyłącznie do celów edukacyjnych i testowych. Używanie go bez wyraźnej zgody użytkownika końcowego może być nielegalne. Autor nie ponosi odpowiedzialności za sposób wykorzystania tego kodu.
