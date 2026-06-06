from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from tensorflow import keras
import os

# Charger le modèle entraîné
model = keras.models.load_model(os.path.join(os.path.dirname(__file__), "..", "models", "modele_orca.keras"))

# Liste des classes, assure-toi qu'elles sont dans le bon ordre
labels = ['Beluga', 'Dauphin', 'Orque']  # Doit correspondre aux classes du modèle

# Afficher les classes des labels
print("Classes des labels :")
for i, label in enumerate(labels):
    print(f"{i}: {label}")

# Charger une nouvelle image (spectrogramme)
image_path = os.path.join(os.path.dirname(__file__), "spectroppourtest", "belugatest1.png")  # Remplace par ton fichier
img = load_img(image_path, target_size=(128, 128))
img_array = img_to_array(img) / 255.0  # Normaliser entre 0 et 1
img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension batch

# Faire une prédiction
prediction = model.predict(img_array)

# Afficher la classe prédite
print(f"Scores bruts de prédiction : {prediction}")
predicted_class = np.argmax(prediction, axis=1)[0]

# Afficher le résultat correctement avec la bonne classe
print(f"Prédiction : {labels[predicted_class]}")