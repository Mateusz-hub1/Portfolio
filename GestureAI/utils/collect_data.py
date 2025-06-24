import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

label = input("Podaj nazwę gestu, np. open, fist, peace: ").strip()
filename = f"data_{label}.csv"

# Opcja: czy na początku wyczyścić plik? (tak, jeśli chcesz czyste dane za każdym razem)
clear_file = input(f"Czy wyczyścić plik {filename} na start? (t/n): ").lower() == 't'
if clear_file and os.path.exists(filename):
    os.remove(filename)
    print(f"Plik {filename} został wyczyszczony.")

cap = cv2.VideoCapture(1)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

data = []

print(f"\nZbieranie danych dla gestu '{label}'.")
print("Wciśnij:")
print("  s - zapisz próbkę (jeśli ręka wykryta)")
print("  c - wyczyść aktualne próbki w sesji")
print("  q - zakończ i zapisz do pliku\n")

while True:
    success, img = cap.read()
    if not success:
        print("Nie udało się odczytać obrazu z kamery.")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Przygotuj dane do zapisu (wszystkie punkty dłoni)
        row = []
        for lm in result.multi_hand_landmarks[0].landmark:
            row.extend([lm.x, lm.y, lm.z])
    else:
        row = None  # brak ręki

    # Tekst na ekranie
    info_text = f"Gest: {label} | Probki w sesji: {len(data)}"
    controls_text = "s=Zapisz | c=Wyczysc sesje | q=Koniec"
    if row is None:
        warning_text = "Brak wykrytej ręki - nie mozna zapisac probki"
        cv2.putText(img, warning_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    cv2.putText(img, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, controls_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    cv2.imshow("Zbieranie gestów", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        if row is not None:
            # Dodaj na koniec etykietę gestu (np. 'open')
            data.append(row + [label])
            print(f"Zapisano próbkę nr {len(data)}")
        else:
            print("Nie wykryto ręki, nie zapisano próbki.")
    elif key == ord('c'):
        data = []
        print("Wyczyszczono próbki w bieżącej sesji.")
    elif key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

        folder = "training_data"
        os.makedirs(folder, exist_ok=True)  # upewniamy się, że folder istnieje
        filename = os.path.join(folder, filename)

        if data:
            mode = 'a' if os.path.exists(filename) else 'w'
            with open(filename, mode, newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print(f"Zapisano {len(data)} próbek do pliku {filename}")
        else:
            print("Brak próbek do zapisania.")
        break
