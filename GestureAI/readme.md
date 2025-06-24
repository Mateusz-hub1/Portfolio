Pewnie! Oto przykładowy plik `README.md` dla Twojego projektu rozpoznawania gestów dłoni przy użyciu sieci neuronowej i danych z plików `.csv`, oparty na bibliotece Keras i MediaPipe:


# Uruchomienie programu (w srodwisku wirtualnym)
Linux/ mac: (wirtualnie)
python3 -m venv venv
source venv/bin/activate

# instalacja niezbednych bibliotek 
pip install -r requirements.txt


# 🤖 Hand Gesture Recognition with Neural Network

Projekt rozpoznawania gestów dłoni w czasie rzeczywistym przy użyciu sieci neuronowej i danych przestrzennych punktów dłoni (MediaPipe). Model uczy się rozpoznawać różne gesty ręki na podstawie współrzędnych 3D i klasyfikuje je do jednej z kilkunastu zdefiniowanych kategorii.

## 🧠 O projekcie

Celem projektu jest stworzenie prostego, ale skutecznego systemu rozpoznawania gestów, który może być używany do:

- sterowania aplikacjami,
- interfejsów użytkownika bezdotykowych (touchless UI),
- wsparcia dla osób z niepełnosprawnościami,
- zabawy lub gier opartych na gestach.

Model został wytrenowany na danych zapisanych w plikach `.csv`, które zawierają 63 cechy (21 punktów dłoni * 3 współrzędne: x, y, z).

## 📁 Struktura projektu

```

gesty/
├── model/                      # Zapisany model .keras
├── training\_data/             # Pliki CSV z danymi dla każdego gestu
│   ├── data\_fist.csv
│   ├── data\_open.csv
│   └── ...
├── utils/
│   └── train\_model.py         # Skrypt do trenowania modelu
├── gesture\_predictor.py       # (opcjonalnie) Klasyfikator do predykcji w czasie rzeczywistym
└── README.md                  # Niniejszy plik

````

## 🧪 Gesty do rozpoznania

Model rozpoznaje następujące gesty dłoni:

1. 👊 Pięść (`fist`)
2. ✋ Otwarta dłoń (`open`)
3. ✌️ Zwycięstwo (`victory`)
4. 🤘 Rock (`rock`)
5. ☝️ Wskazujący palec (`point`)
6. 🖖 Spock (`Spock`)
7. 🤙 Call me (`CallMe`)
8. ✌️✌️ Dwa palce wskazujące (`TwoFingerPoint`)
9. 👆 Kciuk do palca wskazującego (`ThumbToPoint`)
10. 👉 Kciuk do środkowego (`ThumbToMiddle`)
11. 🖕 Środkowy palec (`middleFinger`)

## 🚀 Jak uruchomić

1. **Zainstaluj zależności:**

```bash
pip install -r requirements.txt
````

2. **Trenuj model:**

```bash
python utils/train_model.py
```

3. **Model zostanie zapisany do folderu `model/gesture_model.keras`.**

## 🛠️ Technologie

* Python 3.11+
* TensorFlow / Keras
* NumPy, Pandas
* MediaPipe (do generowania danych gestów)
* scikit-learn (do podziału danych)

## ✅ Przykładowy wynik

```
Liczba próbek: 5500, liczba cech: 63  
Liczba klas: 11  
Test loss: 0.0553, Test accuracy: 0.9817  
Model wytrenowany i zapisany do model/gesture_model.keras
```

## 💡 Pomysły na rozwój

* Dodanie kamery i integracja z MediaPipe w czasie rzeczywistym
* Więcej klas gestów (np. alfabet migowy)
* Eksport modelu do TensorFlow Lite do użycia na urządzeniach mobilnych
* Interfejs graficzny (GUI) do demonstracji gestów

## 📄 Licencja

Projekt edukacyjny, open-source — feel free to fork & modify ✌️

---

🧠 Autor: \[Twoje imię/nick]
📅 Data ostatniej aktualizacji: czerwiec 2025

```

---

Jeśli chcesz, mogę też przygotować wersję po angielsku, dodać grafikę lub diagram działania. Daj znać!
```
