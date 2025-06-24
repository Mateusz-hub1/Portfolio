#  Rozpoznawanie Gestów Dłoni z Siecią Neuronową (TensorFlow + MediaPipe)

Projekt ten umożliwia rozpoznawanie gestów dłoni na podstawie danych 3D punktów z MediaPipe i klasyfikuje je za pomocą sieci neuronowej. Uczy się na danych z plików CSV i może być rozszerzony do obsługi gestów w czasie rzeczywistym.


---

##  Szybki start

### 1. Utwórz i aktywuj środowisko wirtualne (Linux/macOS):
python3 -m venv venv
source venv/bin/activate

### 2. Zainstaluj zależności:
pip install -r requirements.txt

### 3. Wytrenuj model:
python utils/train_model.py

Model zostanie zapisany jako: model/gesture_model.keras

⸻

## O projekcie
	•	 Uczy się 63 cech (21 punktów dłoni × 3 wymiary: x, y, z)
	•	 Dane treningowe w formacie CSV (training_data/)
	•	 Możliwość łatwego rozszerzenia o nowy gest
	•	 Zaprojektowane z myślą o kontroli ruchem, grach i interfejsach bezdotykowych

⸻

## Rozpoznawane gesty
```bash
Nazwa	Opis
fist	👊 Pięść
open	✋ Otwarta dłoń
victory	✌️ Zwycięstwo
rock	🤘 Rock
point	☝️ Wskazujący palec
Spock	🖖 Spock
CallMe	🤙 Call me
TwoFingerPoint	✌️✌️ Dwa palce wskazujące
ThumbToPoint	👆 Kciuk → wskazujący
ThumbToMiddle	👉 Kciuk → środkowy
middleFinger	🖕 Środkowy palec
```

⸻

🗂️ Struktura projektu
```bash
.
├── model/
│   └── gesture_model.keras
├── training_data/
│   ├── data_fist.csv
│   ├── data_open.csv
│   └── ...
├── utils/
│   ├── collect_data.py
│   ├── gestures_control.py
│   └── train_model.py
├── requirements.txt
└── README.md
```

⸻

## Pliki i funkcje

	•	collect_data.py – Zbieranie punktów dłoni do plików .csv
	•	train_model.py – Trening modelu Keras
	•	gestures_control.py – Wykrywanie gestów i kontrolowanie kursora/myszy

⸻

## Przykład wyników
```bash
Liczba próbek: 5500
Liczba cech: 63
Liczba klas: 11
Test accuracy: 0.9817
Model zapisany do model/gesture_model.keras
```


⸻

## Możliwości rozwoju
```bash
	•	Dodanie rozpoznawania gestów na żywo z kamery
	•	Eksport modelu do TensorFlow Lite (np. na Raspberry Pi)
	•	Rozszerzenie o alfabet migowy (ASL)
	•	Stworzenie GUI do testowania
```
⸻
