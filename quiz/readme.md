
# Strona z quizami – wersja przeglądarkowa 
Interaktywny system quizowy działający w przeglądarce, napisany w HTML, CSS i JavaScript. Aplikacja nie wymaga backendu – wszystkie dane są ładowane lokalnie. Obsługuje wiele kategorii quizów, zapis wyników w `localStorage`, tryb ciemny, licznik czasu oraz animacje zwycięstwa (konfetti).
---

##  Główne funkcje

- Dynamiczne ładowanie kategorii quizów z plików JSON (`/data`)
- Zegar kołowy z odliczaniem (25 minut)
- Obsługa multimediów w pytaniach (grafiki, wideo)
- Śledzenie poprawności odpowiedzi, streaków i punktacji
- System zapisu wyników do `localStorage` z rankingiem
- Tryb ciemny i jasny (zmiana w locie)
- Animacje konfetti po ukończeniu quizu

---

##  Uruchomienie lokalne

    1. Sklonuj repozytorium:
    git clone https://github.com/Mateusz-hub1/nazwa-repozytorium.git
  	2.	Otwórz index.html w przeglądarce:
      	•	Kliknij dwukrotnie lub
      	•	Użyj Live Server (np. w Visual Studio Code)
  	3.	Wybierz kategorię quizu z listy i rozpocznij grę.

⸻

   Dodawanie nowych quizów
	1.	Skopiuj jeden z plików w /data, np. historia_pl.json
	2.	Nadaj nową nazwę, np. chemia.json
	3.	Zaktualizuj jego zawartość (ID, tytuł, pytania, odpowiedzi)
	4.	Dodaj nazwę pliku do tablicy FILES w app.js:

const FILES = ['prawo_jazdy', 'egzamin_it', 'historia_pl', 'chemia'];


⸻

 Dane użytkownika

Wszystkie dane użytkownika (imię, wynik, czas, streak) są zapisywane lokalnie w localStorage. Strona nie przesyła żadnych danych na zewnątrz.

⸻
