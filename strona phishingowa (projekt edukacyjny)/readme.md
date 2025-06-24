# Symulacja strony phishingowej – edukacyjny projekt HTML/CSS/JS

Ten projekt przedstawia interaktywną, front-endową symulację strony phishingowej stylizowanej na logowanie do serwisu społecznościowego. Został stworzony wyłącznie w celach edukacyjnych, demonstracyjnych oraz uświadamiających – nie realizuje żadnych działań ofensywnych.

---

##  Cel projektu

- Zademonstrowanie, jak wyglądają typowe strony phishingowe
- Testowanie mechanizmów socjotechnicznych (np. fałszywe komunikaty)
- Zbieranie danych testowych do zewnętrznych arkuszy (Google Sheets)
- Prezentacja front-endowych technik stylizacji i responsywności

---

##  Technologie

- HTML5
- CSS3 (responsywny layout, stylizacja mobilna)
- JavaScript (walidacja formularza, fetch API, localStorage)
- Google Apps Script (do odbierania danych z formularza)

---

##  Jak to działa?

1. Użytkownik widzi ekran przypominający formularz logowania.
2. Po wpisaniu danych (e-mail + hasło) i kliknięciu "Zaloguj się":
   - dane trafiają do `Google Apps Script` (w formacie `FormData`)
   - wyświetlany jest komunikat błędu w stylu: *"Błędny login..."*
3. Dołączony jest również popup z informacją o plikach cookie, zgodnie z aktualnymi UX-praktykami.

---

## ⚙ Uruchomienie

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/Mateusz-hub1/nazwa-repozytorium.git

	2.	Otwórz index.html w przeglądarce (najlepiej przez Live Server).

⸻

Integracja z Google Sheets

Formularz przesyła dane (email + password) do wskazanego Apps Script. Wymaga aktywnego endpointa (np. https://script.google.com/macros/s/.../exec) i skonfigurowanego skryptu Google Apps Script.

⸻

 Responsywność

Strona zawiera pełne wsparcie dla ekranów mobilnych (media queries), co pozwala testować zachowanie na różnych rozdzielczościach – od desktopu po telefony.

⸻

🛑 Ważne

Ten projekt nie służy do atakowania użytkowników. Nie zawiera funkcji ukrywania, replikowania domen czy omijania zabezpieczeń. Może być wykorzystywany wyłącznie w celach:
	•	demonstracyjnych (np. na szkoleniach z cyberbezpieczeństwa),
	•	testowych (np. jako honeypot UI),
	•	edukacyjnych (np. do analizy ataków phishingowych).

⸻
