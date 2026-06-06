import tensorflow as tf
import pandas as pd
import numpy as np
import os
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Chemins
CSV_FILE = "labels.csv"
IMAGE_DIR = "spectrograms"

# Charger le fichier CSV
df = pd.read_csv(CSV_FILE)

# Récupérer les labels uniques et les encoder en nombres
labels = sorted(df["label"].unique())  # Trier pour garder un ordre cohérent
label_to_index = {label: i for i, label in enumerate(labels)}  # Ex: {"orque": 0, "dauphin": 1, ...}

# Charger les images et leurs labels
images = []
targets = []

for _, row in df.iterrows():
    image_path = os.path.join(IMAGE_DIR, row["file_name"])
    if os.path.exists(image_path):
        img = load_img(image_path, target_size=(128, 128))  # Redimensionner les images
        img_array = img_to_array(img) / 255.0  # Normaliser entre 0 et 1
        images.append(img_array)
        targets.append(label_to_index[row["label"]])

# Convertir en tableaux numpy
X = np.array(images)
y = np.array(targets)
y = to_categorical(y, num_classes=len(labels))  # One-hot encoding

# Afficher quelques stats
print(f"✅ Données chargées : {X.shape[0]} images de taille {X.shape[1:]} avec {len(labels)} classes.")

# Sauvegarde pour entraînement
np.save("X.npy", X)
np.save("y.npy", y)
