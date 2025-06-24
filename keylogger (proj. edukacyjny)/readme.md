# Keylogger z zapisem do Google Sheets

Ten projekt to edukacyjny keylogger napisany w Pythonie, który rejestruje naciśnięcia klawiszy i zapisuje je do arkusza Google Sheets za pomocą API. Działa w środowisku wirtualnym, z obsługą szyfrowania lokalnych logów oraz buforowaniem.

## Wymagania

- Python 3.8+
- Połączenie z internetem
- Utworzone konto serwisowe w Google Cloud z dostępem do Google Sheets API
- Plik `service_account.json` pobrany z Google Cloud Console
- Arkusz Google Sheets udostępniony temu kontu

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki:

git clone https://github.com/twoj-uzytkownik/keylogger.git
cd keylogger

	2.	Utwórz i aktywuj środowisko wirtualne:

python3 -m venv venv
source venv/bin/activate

	3.	Zainstaluj zależności:

pip install -r requirements.txt

	4.	Utwórz plik .env na podstawie wzoru .env.example:

cp .env.example .env

Uzupełnij plik .env danymi:
	•	SERVICE_ACCOUNT_FILE – ścieżka do pliku JSON z Google Cloud
	•	SPREADSHEET_ID – ID arkusza z URL Google Sheets
	•	WORKSHEET_NAME – nazwa zakładki (np. Arkusz1)
	•	FERNET_KEY – klucz szyfrujący (opcjonalny)
	•	DURATION_S, FLUSH_EVERY_N_KEYS, FLUSH_EVERY_SEC – parametry działania

Uruchomienie programu

W aktywnym środowisku:

python keylogger_cloud.py

Logi z naciśnięć będą przesyłane do wskazanego arkusza Google Sheets.

Uwagi

Projekt ma charakter wyłącznie edukacyjny. Nie należy wykorzystywać go bez wyraźnej zgody właściciela systemu docelowego. Wszelkie działania należy prowadzić zgodnie z obowiązującym prawem.

