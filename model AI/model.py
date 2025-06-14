import os

#Wyłączenie ostrzeżeń związanych z przestarzałą wersją Tk na macOS
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from openai import OpenAI

client = OpenAI(api_key="KLUCZ API")
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import webbrowser
import tabula 

###############################################################################
# KONFIGURACJA OPENAI
###############################################################################

#if not OpenAI.api_key:
#    raise ValueError("Klucz API nie został ustawiony poprawnie.")

###############################################################################
# ZMIENNE GLOBALNE
###############################################################################
last_report_file = None  # Na ścieżkę do ostatniego wygenerowanego raportu
selected_mode = None     # Zmienna do przechowywania wybranego trybu (Pentester / Analizator logów)
output_text = None       # Referencja do pola tekstowego w dolnym panelu
input_text = None        # Referencja do pola tekstowego z danymi wejściowymi

###############################################################################
# FUNKCJE POMOCNICZE
###############################################################################
def log_error(error_message: str):
    """
    Zapisuje komunikat błędu do pliku `error_log.txt` wraz ze znacznikiem czasu.
    Przydaje się do debugowania wyjątków w aplikacji.
    """
    try:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {error_message}\n")
    except Exception as log_ex:
        print(f"[!] Nie udało się zapisać do error_log.txt: {log_ex}")

def update_output(text: str):
    """
    Aktualizuje pole tekstowe 'output_text', wyświetlając przekazany tekst.
    Czyści poprzednią zawartość i wstawia nową (pole jest w trybie DISABLED).
    """
    global output_text
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)
    print(f"[DEBUG] update_output wywołane z tekstem:\n{text}")  # Debug

###############################################################################
# FUNKCJE LOGIKI PENTESTERA
###############################################################################
def pentester_function(user_input: str):
    """
    Funkcja Pentestera:

      - Wysyła zapytanie do ChatCompletion (OpenAI) na podstawie `user_input`.
      - Analizuje odpowiedź i podejmuje odpowiednie działania.
      - Obsługuje różne scenariusze pentestingu, takie jak:
        - Generowanie raportów z luk bezpieczeństwa
        - Propozycje ataków i metod obrony
        - Analiza konfiguracji systemów
        - Tworzenie skryptów do automatyzacji zadań pentestera
      - W razie błędu, zapisuje go do pliku `error_log.txt` i zwraca komunikat w `output_text`.
    """
    global output_text
    print("[DEBUG] Wywołano pentester_function()")  # Debug
    try:
        # Tworzymy zapytanie do modelu GPT-3.5 (lub GPT-4, jeśli masz dostęp).
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pentesterem. Wykonuj testy penetracyjne."},
            {"role": "user", "content": user_input},
        ],
        max_tokens=500,
        temperature=0.7)
        output_content = response.choices[0].message.content.strip()

        # Opcjonalnie: sprawdź liczbę zużytych tokenów
        usage_info = ""
        if "usage" in response:
            total_tokens = response.usage.get("total_tokens", None)
            if total_tokens:
                usage_info = f"\n\n[INFO] Zużyte tokeny: {total_tokens}"

        update_output(f"Wynik Pentestera:\n{output_content}{usage_info}")

    except Exception as e:
        error_message = f"Błąd Pentestera: {str(e)}"
        update_output(error_message)
        log_error(error_message)

###############################################################################
# FUNKCJE LOGIKI ANALIZATORA LOGÓW
###############################################################################
def analyze_logs(logs: pd.DataFrame):
    """
    Funkcja analizy logów:
      - Filtruje logi dla kilku poziomów severity (np. ERROR, CRITICAL, WARNING),
      - Zapisuje wyniki do pliku 'anomalies_report_<data>.csv',
      - Prezentuje wykres wystąpień anomalii (matplotlib).
    """
    global output_text, last_report_file
    print("[DEBUG] Wywołano analyze_logs()")  # Debug
    try:
        # Sprawdzamy czy kolumna 'severity' istnieje w DataFrame
        if "severity" not in logs.columns:
            update_output("Plik logów nie zawiera kolumny 'severity'.")
            return

        # Filtrujemy przykładowe poziomy (możesz dostosować do własnych potrzeb)
        severity_levels = ["ERROR", "CRITICAL", "WARNING"]
        anomalies = logs[logs["severity"].isin(severity_levels)]

        # Generujemy dynamiczną nazwę pliku raportu
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"anomalies_report_{timestamp}.csv"
        anomalies.to_csv(report_filename, index=False)

        # Komunikat o liczbie anomalii i zapisie pliku
        info_text = (
            f"Znaleziono {len(anomalies)} anomalii.\n"
            f"Raport zapisany jako: {report_filename}\n"
            "Możesz go teraz otworzyć lub przejrzeć w dowolnym edytorze CSV."
        )
        update_output(info_text)

        # Wyświetlamy prosty wykres rozkładu anomalii
        plt.figure(figsize=(6, 4))
        anomalies["severity"].value_counts().plot(kind="bar", color='skyblue')
        plt.title("Rozkład anomalii (ERROR/CRITICAL/WARNING)")
        plt.xlabel("Typ błędu")
        plt.ylabel("Liczba wystąpień")
        plt.tight_layout()
        plt.show()

        # Zapisujemy nazwę pliku w zmiennej globalnej (by móc go otworzyć później)
        last_report_file = os.path.abspath(report_filename)

    except Exception as e:
        error_message = f"Błąd podczas analizy logów: {str(e)}"
        update_output(error_message)
        log_error(error_message)


def parse_file_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Funkcja pomocnicza do wczytania pliku w zależności od rozszerzenia
    i zwrócenia go jako DataFrame (lub podniesienia błędu w razie problemów).
    Obsługiwane formaty: CSV, JSON, XML, HTML, PDF.
    """
    # Rozpoznajemy rozszerzenie pliku
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == ".csv":
        # Wczytanie CSV
        return pd.read_csv(file_path)

    elif file_extension == ".json":
        # Wczytanie JSON
        return pd.read_json(file_path)

    elif file_extension == ".xml":
        # Wczytanie XML (Pandas >= 1.3)
        return pd.read_xml(file_path)

    elif file_extension in (".html", ".htm"):
        # pd.read_html zwraca listę DataFrame'ów (dla każdej znalezionej tabeli)
        dfs = pd.read_html(file_path)
        if len(dfs) > 0:
            # W przykładzie pobieramy pierwszą tabelę
            return dfs[0]
        else:
            raise ValueError("Nie znaleziono tabel w pliku HTML.")

    elif file_extension == ".pdf":
        # Wczytanie PDF – wymaga tabula-py lub innej biblioteki do konwersji
        # convert_into() tworzy plik tymczasowy w formacie CSV, który następnie wczytujemy
        temp_csv = f"temp_{os.getpid()}.csv"
        try:
            tabula.convert_into(file_path, temp_csv, output_format="csv", pages="all")
            if os.path.exists(temp_csv):
                df = pd.read_csv(temp_csv)
                os.remove(temp_csv)
                return df
            else:
                raise FileNotFoundError("Nie udało się utworzyć pliku tymczasowego CSV.")
        except Exception as e:
            raise ValueError(f"Problem z przetwarzaniem PDF: {str(e)}")

    else:
        raise ValueError(f"Nieobsługiwane rozszerzenie pliku: {file_extension}")


def log_analyzer_function():
    """
    Funkcja Analizatora logów: umożliwia wybór pliku w różnych formatach
    (CSV, JSON, XML, HTML, PDF) i wywołuje funkcję analyze_logs().
    """
    print("[DEBUG] Wywołano log_analyzer_function()")  # Debug
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("CSV Files", "*.csv"),
            ("JSON Files", "*.json"),
            ("XML Files", "*.xml"),
            ("HTML Files", "*.html;*.htm"),
            ("PDF Files", "*.pdf"),
            ("Wszystkie pliki", "*.*"),
        ]
    )
    if not file_path:
        update_output("Nie wybrano pliku.")
        return

    try:
        logs_df = parse_file_to_dataframe(file_path)
        analyze_logs(logs_df)
    except Exception as e:
        error_message = f"Błąd podczas wczytywania pliku: {str(e)}"
        update_output(error_message)
        log_error(error_message)

###############################################################################
# FUNKCJE AKCJI / OBSŁUGI GUI
###############################################################################
def process_input():
    """
    Wywołuje odpowiednią funkcję w zależności od wybranego trybu (Pentester / Analizator logów).
    """
    print("[DEBUG] Wywołano process_input()")  # Debug
    user_data = input_text.get("1.0", "end-1c").strip()  # Pobierz dane z pola tekstowego
    mode = selected_mode.get()
    print(f"[DEBUG] Aktualny tryb: {mode}")  # Debug

    if mode == "Pentester":
        if not user_data:
            update_output("Proszę wprowadzić dane wejściowe dla Pentestera.")
            return
        pentester_function(user_data)

    elif mode == "Analizator logów":
        log_analyzer_function()

    else:
        update_output("Wybierz najpierw tryb pracy (Pentester / Analizator logów).")

def save_output_to_file():
    """
    Zapisuje tekst z 'output_text' do pliku tekstowego (.txt).
    """
    global output_text
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        update_output("Brak treści do zapisania.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            update_output(f"Wynik został zapisany do: {file_path}")
        except Exception as e:
            error_message = f"Błąd podczas zapisywania pliku: {str(e)}"
            update_output(error_message)
            log_error(error_message)

def clear_input():
    """
    Czyści zawartość pola tekstowego z danymi wejściowymi.
    """
    print("[DEBUG] Wywołano clear_input()")  # Debug
    input_text.delete("1.0", tk.END)

def clear_output():
    """
    Czyści treść w polu tekstowym 'output_text'.
    """
    global output_text
    print("[DEBUG] Wywołano clear_output()")  # Debug
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)

def show_help():
    """
    Wyświetla okno z informacjami pomocy.
    """
    help_message = (
        "Pomoc:\n\n"
        "1. Wybierz tryb: Pentester lub Analizator logów.\n"
        "2. Jeśli wybrano Pentester, wpisz komendę/zapytanie w polu 'Dane wejściowe'.\n"
        "3. Jeśli wybrano Analizator logów, wczytaj plik CSV do analizy.\n"
        "4. Użyj przycisku 'Rozpocznij pracę' do wykonania wybranej akcji.\n\n"
        "Dodatkowe funkcje:\n"
        "- 'Zapisz wynik do pliku': zapisuje treść wyjściową do pliku tekstowego.\n"
        "- 'Wyczyść dane wejściowe': czyści pole tekstowe dla danych wejściowych.\n"
        "- 'Wyczyść wynik': czyści pole wyświetlające wyniki.\n"
        "- 'Otwórz raport anomalii': otwiera ostatnio wygenerowany raport z anomaliami CSV (o ile istnieje).\n"
    )
    messagebox.showinfo("Pomoc", help_message)

def open_anomalies_report():
    """
    Otwiera ostatnio wygenerowany plik z raportem anomalii CSV (o ile istnieje).
    Uruchamia domyślną przeglądarkę / edytor CSV w systemie.
    """
    global last_report_file
    print("[DEBUG] Wywołano open_anomalies_report()")  # Debug
    if last_report_file and os.path.exists(last_report_file):
        webbrowser.open(f"file://{last_report_file}")
    else:
        update_output("Nie znaleziono ostatniego raportu lub nie został jeszcze wygenerowany.")

###############################################################################
# KONFIGURACJA UI - TKINTER
###############################################################################
print("[DEBUG] Tworzenie okna głównego...")  # Debug
root = tk.Tk()
root.title("Pentester & Log Analyzer")
root.geometry("900x500")
root.resizable(True, True)

# Ustaw kolor tła głównego okna (np. czarny)
root.configure(bg="#140f0f")

# Inicjalizacja zmiennych globalnych:
selected_mode = tk.StringVar(value="Pentester")

######################
# GÓRNY PANEL: WYBÓR TRYBU
######################
mode_frame = tk.Frame(root, bg="#140f0f")
mode_frame.pack(fill="x", pady=10)

mode_label = tk.Label(mode_frame, text="Wybierz tryb pracy:", font=("Arial", 12), bg="#322323")
mode_label.pack(side="left", padx=(20, 10))

pentester_button = tk.Button(mode_frame, text="Pentester", command=lambda: selected_mode.set("Pentester"), width=15)
pentester_button.pack(side="left", padx=(10, 5))

log_analyzer_button = tk.Button(mode_frame, text="Analizator logów", command=lambda: selected_mode.set("Analizator logów"), width=15)
log_analyzer_button.pack(side="left", padx=5)

######################
# ŚRODKOWY PANEL: DANE WEJŚCIOWE
######################
input_frame = tk.Frame(root, bg="#281e1e")
input_frame.pack(fill="x", pady=5)

input_label = tk.Label(input_frame, text="Dane wejściowe:", font=("Arial", 14), bg="#281e1e", fg="#ffffff", )
input_label.pack(anchor="w", padx=(20, 0), pady=(5, 5))

input_text = tk.Text(input_frame, height=8, width=90, wrap="word", bg="#281e1e", fg="#ffffff")
input_text.pack(padx=20, pady=(0, 5))

clear_input_button = tk.Button(input_frame, text="Wyczyść dane wejściowe", command=clear_input, width=20)
clear_input_button.pack(anchor="e", padx=20, pady=(0, 10))

######################
# PRZYCISKI AKCJI
######################
action_frame = tk.Frame(root, bg="#3c3232")
action_frame.pack(fill="x", pady=5)

process_button = tk.Button(action_frame, text="Rozpocznij pracę", command=process_input, width=20, bg="#c83232")
process_button.pack(side="left", padx=(20, 5), pady=10)

save_button = tk.Button(action_frame, text="Zapisz wynik do pliku", command=save_output_to_file, width=20, highlightcolor="#46c832")
save_button.pack(side="left", padx=5, pady=10)

open_report_button = tk.Button(action_frame, text="Otwórz raport anomalii", command=open_anomalies_report, width=20, bg="#46c878")
open_report_button.pack(side="left", padx=5, pady=10)

help_button = tk.Button(action_frame, text="Pomoc", command=show_help, width=10, bg="#463278")
help_button.pack(side="left", padx=5, pady=10)

######################
# DOLNY PANEL: WYNIK
######################
output_frame = tk.Frame(root, bg="#281e1e")
output_frame.pack(fill="both", expand=True, pady=(5, 10))

output_label_title = tk.Label(output_frame, text="Wynik:", font=("Arial", 14, "bold"), bg="#281e1e", fg="#ffffff")
output_label_title.pack(anchor="w", padx=20, pady=(0, 5))

output_text = tk.Text(
    output_frame,
    wrap="word",
    bg="#463232",
    fg="#ffffff",
    width=90,
    height=15,
    state=tk.DISABLED
)
output_text.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 5))

# Dodajemy scrollbar pionowy
output_scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
output_scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=output_scrollbar.set)

clear_output_button = tk.Button(output_frame, text="Wyczyść wynik", command=clear_output, width=40)
clear_output_button.pack(anchor="e", padx=20, pady=(5, 0))

print("[DEBUG] Uruchamianie pętli głównej...")  # Debug
root.mainloop()