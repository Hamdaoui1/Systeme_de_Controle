import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Répertoire contenant les fichiers CSV de données
data_dir = "data"

# Charger les données à partir des fichiers CSV
def load_data(data_dir):
    features = []
    labels = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".csv"):
            label = file_name.replace(".csv", "").replace("/", "_")  # Remplacer / par _ dans les labels
            data = pd.read_csv(os.path.join(data_dir, file_name), header=None)
            # Ajouter les distances et les labels
            features.append(data.iloc[:, 1:].values)
            labels.extend([label] * len(data))
    features = np.vstack(features)  # Combiner toutes les caractéristiques
    return features, labels

# Mapper les labels (ex. "play_pause" -> 0, "augmenter_le_volume" -> 1, etc.)
def encode_labels(labels):
    unique_labels = sorted(set(labels))
    label_to_index = {label: idx for idx, label in enumerate(unique_labels)}
    return np.array([label_to_index[label] for label in labels]), label_to_index

# Charger et préparer les données
features, labels = load_data(data_dir)
labels, label_to_index = encode_labels(labels)

# Diviser les données en ensemble d'entraînement et de validation
X_train, X_val, y_train, y_val = train_test_split(features, labels, test_size=0.2, random_state=42)

# Normaliser les données (important pour les modèles neuronaux)
X_train = X_train / np.max(X_train, axis=0)
X_val = X_val / np.max(X_val, axis=0)

# Ajouter une caractéristique directionnelle pour distinguer "augmenter le volume" et "diminuer le volume"
def add_directional_feature(data):
    direction = np.sign(data[:, 0] - data[:, 1])  # Ex. : thumb vs index
    return np.hstack((data, direction.reshape(-1, 1)))

X_train = add_directional_feature(X_train)
X_val = add_directional_feature(X_val)

# Transformer les labels en one-hot encoding
y_train = to_categorical(y_train, num_classes=len(label_to_index))
y_val = to_categorical(y_val, num_classes=len(label_to_index))

# Construire le modèle
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(len(label_to_index), activation="softmax")
])

# Compiler le modèle
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Entraîner le modèle
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=32)

# Sauvegarder le modèle
model.save("gesture_recognition_model.h5")
print("Modèle sauvegardé sous 'gesture_recognition_model.h5'.")

# Afficher le mappage des labels
print("Label mapping:", label_to_index)
