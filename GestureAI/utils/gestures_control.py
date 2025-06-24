import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import tensorflow as tf
import time
import ctypes
import os 

#definiowanie funkcji wylogowania z iwndowsa 
def lock_windows():
    ctypes.windll.user32.LockWorkStation()


# === Ładowanie modelu ===
model = tf.keras.models.load_model('model/gesture_model.keras')

# === Ustawienia MediaPipe ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# === Mapa gestów ===
gesture_names = {
    0: "fist",              # Kopiuj (Ctrl+C)
    1: "middlefinger",      # Zablokuj komputer (Win+L)
    2: "open",              # Pauza/Wznów (Spacja)
    3: "thumb_to_middle",   # Prawy klik
    4: "thumb_to_point",    # Lewy klik
    5: "victory",           # Alt+Tab (przełącz okno)
    6: "rock",              # Otwórz Notatnik
    7: "callme",            # Nowa karta w Chrome (Ctrl+T)
    8: "point",             # Strona w górę
    9: "two_fingers",       # Strona w dół
    10: "spock",            # Minimalizuj okna (Win+D)
    11: "pinch",            # Screenshot (Win+Shift+S)
}

# === Przypisanie akcji ===
def perform_action(gesture_id):
    gesture = gesture_names[gesture_id]
    print(f"[INFO] Rozpoznano gest: {gesture}")

    if gesture_id == 0:  # Fist
        pyautogui.hotkey('ctrl', 'c')  # Kopiuj
    elif gesture_id == 1:  # Middle finger
        lock_windows() 
    elif gesture_id == 2:  # Open hand
        pyautogui.press('space')       # Pauza/Wznów
    elif gesture_id == 3:  # Thumb to middle
        pyautogui.click(button='right')
    elif gesture_id == 4:  # Thumb to point
        pyautogui.click(button='left')
    elif gesture_id == 5:  # Victory
        pyautogui.hotkey('alt', 'tab')
    elif gesture_id == 6:  # Rock
        os.system('start notepad')     # Uruchom Notatnik
    elif gesture_id == 7:  # Call Me
        pyautogui.hotkey('ctrl', 't')  # Nowa karta w Chrome
    elif gesture_id == 8:  # Point
        pyautogui.press('pageup')      # Strona w górę
    elif gesture_id == 9:  # Two fingers
        pyautogui.press('pagedown')    # Strona w dół
    elif gesture_id == 10:  # Spock
        pyautogui.hotkey('win', 'd')   # Minimalizuj wszystkie okna
    elif gesture_id == 11:  # Pinch (screen)
        pyautogui.hotkey('win', 'shift', 's')  # Screenshot

# === Przetwarzanie landmarków ===
def extract_landmarks(hand_landmarks):
    return np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]).flatten()

# === Ustawienia ===
cooldown = 2.0  # sekundy
prev_gesture = None
last_action_time = time.time()
action_mode = True  # True = wykonuj akcje, False = tylko podgląd

# === Inicjalizacja kamery ===
cap = cv2.VideoCapture(1)

print("[INFO] Wciśnij 'm', by przełączać tryb działania (podgląd / akcje). ESC = wyjście.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Przetwarzanie obrazu
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        current_gesture_name = "Brak"
        predicted_prob = 0

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = extract_landmarks(hand_landmarks)

                if landmarks.shape[0] == 63:
                    input_data = np.expand_dims(landmarks, axis=0)
                    prediction = model.predict(input_data, verbose=0)
                    gesture_id = np.argmax(prediction)
                    predicted_prob = np.max(prediction)
                    current_gesture_name = gesture_names[gesture_id]

                    if gesture_id != prev_gesture or time.time() - last_action_time > cooldown:
                        if action_mode:
                            perform_action(gesture_id)
                        prev_gesture = gesture_id
                        last_action_time = time.time()

        # === UI: Wyświetlanie informacji ===
        mode_text = "TRYB: " + ("AKCJE" if action_mode else "PODGLĄD")
        cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
        cv2.putText(frame, f"GEST: {current_gesture_name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.putText(frame, f"PEWNOSC: {predicted_prob:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

        cv2.imshow("Sterowanie gestami [ESC=wyjście, M=tryb]", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == ord('m'):
            action_mode = not action_mode
            print(f"[INFO] Przełączono tryb na: {'AKCJE' if action_mode else 'PODGLĄD'}")

finally:
    cap.release()
    cv2.destroyAllWindows()
