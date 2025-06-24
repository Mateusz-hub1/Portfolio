#Ransomware – edukacyjny projekt szyfrowania plików

Ten projekt to prosty, lokalny symulator ransomware napisany w Pythonie. Program szyfruje pliki w zadanym folderze przy użyciu algorytmu `Fernet` z biblioteki `cryptography`, generuje ransomenote, a następnie umożliwia wprowadzenie klucza deszyfrującego. Dodatkowo, dane szyfrowania (ID + klucz) wysyłane są do Google Sheets przez Google Apps Script.

---

##  Jak działa

1. Generowany jest losowy 32-bajtowy klucz szyfrowania i jego skrócone ID (SHA256).
2. Klucz i ID są przesyłane do zdalnego arkusza Google Sheets przez `requests`.
3. Pliki w folderze są szyfrowane (z nadaniem rozszerzenia `.encrypted`).
4. Tworzony jest plik `RANSOM_NOTE.txt` z komunikatem o okupie.
5. Użytkownik ma 3 próby podania klucza. W przypadku niepowodzenia pliki są usuwane.

---

##  Wymagania
- Python 3.10+
- Biblioteki: `cryptography`, `requests`
- Aktywne połączenie z internetem (dla komunikacji z Google Sheets)
- Własny adres `API_URL` do Google Apps Script (jeśli chcesz zbierać klucze)

---

## Instalacja i uruchomienie

    1. Utwórz i aktywuj środowisko:
   
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

	2.	Zainstaluj zależności:

pip install -r requirements.txt

	3.	Ustaw ścieżkę folderu docelowego do szyfrowania w zmiennej TARGET_FOLDER:

TARGET_FOLDER = "/pełna/ścieżka/do/folderu"

	4.	Uruchom program:

python3 nazwa.py

⸻

Zastrzeżenie

Projekt ma charakter edukacyjny. Symuluje zachowanie ransomware lokalnie na plikach testowych. Nie zawiera żadnych mechanizmów ukrywania się, infekowania systemu ani realnych technik złośliwego oprogramowania. Całość działa transparentnie – klucz nie jest ukrywany przed użytkownikiem.

⸻
