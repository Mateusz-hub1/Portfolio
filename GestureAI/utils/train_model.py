import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping



# Ścieżka do folderu z danymi treningowymi (względem lokalizacji tego pliku)
data_folder = os.path.join(os.path.dirname(__file__), '..', 'training_data')
# Definicja etykiet gestów
gest_labels = {
    os.path.join(data_folder, "data_fist.csv"): 0,
    os.path.join(data_folder, "data_middleFinger.csv"): 1,
    os.path.join(data_folder, "data_open.csv"): 2,
    os.path.join(data_folder, "data_ThumbToMiddle.csv"): 3,
    os.path.join(data_folder, "data_ThumbToPoint.csv"): 4,
    os.path.join(data_folder, "data_victory.csv"): 5,
    os.path.join(data_folder, "data_rock.csv"): 6,
    os.path.join(data_folder, "data_CallMe.csv"): 7,
    os.path.join(data_folder, "data_point.csv"): 8,
    os.path.join(data_folder, "data_TwoFingerPoint.csv"): 9,
    os.path.join(data_folder, "data_Spock.csv"): 10,
}
# Wczytywanie danych
X = []
y = []

for file, label in gest_labels.items():
    df = pd.read_csv(file, header=None)
    df = df.iloc[:, :-1]  # usuń ostatnią kolumnę (tekstowa etykieta)
    df = df.astype(float)
    X.append(df.values)
    y += [label] * len(df)

X = np.vstack(X)
y = np.array(y)
y_cat = to_categorical(y)

print(f"Liczba próbek: {X.shape[0]}, liczba cech: {X.shape[1]}")
print(f"Liczba klas: {len(gest_labels)}")

# Podział na train, val i test
X_train, X_temp, y_train, y_temp = train_test_split(X, y_cat, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)




# Definicja modelu
model = Sequential([
    Input(shape=(63,)), # 21 punktów * 3 współrzędne (x,y,z)
    Dense(1024, activation='relu'), #dense- ilsoc neuronow
    BatchNormalization(),
    Dropout(0.4),
    Dense(512, activation='relu'),
    BatchNormalization(),
    Dropout(0.4),
    Dense(11, activation='softmax')
])

# Kompilacja modelu
optimizer = Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Podsumowanie modelu
model.summary()

# Callback EarlyStopping
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Trening
model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=200,#liczba epok (przejsc do nauki sieci neuronowej)
    batch_size=256, #okresenie ilosci probek do jednej epoki
    callbacks=[early_stopping]
)

# Ewaluacja na zbiorze testowym
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test loss: {loss:.4f}, Test accuracy: {accuracy:.4f}")

# Zapisywanie modelu
if not os.path.exists('model'):
    os.makedirs('model')

model.save("model/gesture_model.keras")
print("Model wytrenowany i zapisany do model/gesture_model.keras")
