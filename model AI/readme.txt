# Pentester & Log Analyzer (OpenAI-powered)

Ten projekt to połączenie dwóch funkcjonalności w jednym narzędziu: prostego pentestera wykorzystującego OpenAI oraz analizatora logów systemowych. Aplikacja posiada graficzny interfejs oparty na tkinterze i umożliwia zarówno wysyłanie zapytań do modelu GPT-3.5/4, jak i analizę plików logów z wykrywaniem anomalii.

### Tryb 1 – Pentester

Tryb Pentester umożliwia zadawanie poleceń sztucznej inteligencji działającej jako asystent testów penetracyjnych. Na podstawie podanego zapytania AI:

- generuje raporty z potencjalnych podatności,
- proponuje scenariusze ataków i metody obrony,
- analizuje konfiguracje systemowe,
- sugeruje automatyzację prostych zadań pentesterskich (skrypty, payloady, itd.).

Działa na silniku OpenAI `gpt-3.5-turbo`, z możliwością dostosowania do `gpt-4` przy posiadaniu dostępu.

### Tryb 2 – Analizator logów

Drugi tryb to prosty analizator plików logów w formatach:
`CSV`, `JSON`, `XML`, `HTML`, `PDF`.

Na podstawie kolumny `severity` wykrywa logi oznaczone jako:
- `ERROR`
- `CRITICAL`
- `WARNING`

Dla znalezionych anomalii generowany jest plik CSV z raportem oraz prosty wykres statystyczny. Użytkownik może go zapisać i otworzyć w domyślnej aplikacji systemowej.

---

##  Technologie

- Python 3.10+
- OpenAI API (via `openai` lib)
- tkinter (GUI)
- pandas, matplotlib
- tabula-py (PDF parser)

---

##  Uruchamianie

	1. Skonfiguruj środowisko:

pip install -r requirements.txt

	2.	Ustaw swój klucz API OpenAI (np. w kodzie lub jako zmienna środowiskowa):

export OPENAI_API_KEY=twoj_klucz

	3.	Uruchom aplikację:

python app.py


⸻

📁 Obsługiwane formaty logów

Format pliku	Obsługa
.csv	✔️ pandas
.json	✔️ pandas
.xml	✔️ pandas (read_xml)
.html	✔️ pandas (read_html)
.pdf	✔️ tabula-py


⸻

Dlaczego ten projekt?

Chciałem przetestować praktyczne połączenie interfejsu AI z zadaniami typowo technicznymi – w tym przypadku pentestingiem i analizą logów. To narzędzie może służyć jako punkt wyjścia do większych projektów związanych z bezpieczeństwem. Dodatkowo byl on projektem realizowanym w ramach konkursu ROARING hackaton.

⸻

Projekt jest edukacyjny. Nie służy do przeprowadzania nieautoryzowanych testów penetracyjnych ani nie powinien być wykorzystywany w sposób sprzeczny z prawem.

---

Jeśli chcesz, mogę też dorzucić `requirements.txt`, mockowe `logi.csv`, grafikę GUI do README albo dodać badge'y (`python version`, `license`, `stars`, itd.). Daj znać, co dalej!
