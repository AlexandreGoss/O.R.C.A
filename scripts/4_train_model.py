import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Charger les données
X = np.load("X.npy")
y = np.load("y.npy")

# Paramètres
IMG_SHAPE = X.shape[1:]  # (128, 128, 3)
NUM_CLASSES = y.shape[1]  # Nombre de classes

# Création du modèle réseau de neurones convolutionnel (CNN)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=IMG_SHAPE),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Pour éviter l'overfitting
    Dense(NUM_CLASSES, activation='softmax')  # Softmax pour la classification multi-classes
])

# Compilation du modèle
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Affichage du résumé
model.summary()

# Entraînement du modèle
history = model.fit(X, y, epochs=20, batch_size=8, validation_split=0.2)

# Sauvegarde du modèle
model.save("modele_orca.keras")

# Affichage des courbes d'entraînement
plt.plot(history.history['accuracy'], label="Train Accuracy")
plt.plot(history.history['val_accuracy'], label="Validation Accuracy")
plt.xlabel("Époques")
plt.ylabel("Précision")
plt.legend()
plt.show()
