# ORCA - Ocean Research & Cetacean Acoustics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [Français](#français)

---

## English

ORCA is a bioacoustics project that uses artificial intelligence to identify cetacean species (orcas, dolphins, belugas) from underwater audio recordings.

### Objective

The web application allows you to upload an audio file (`.mp3`, `.wav`) and uses a Deep Learning model (CNN) to predict the most likely species present in the recording.

### Features

- **Audio file upload**: Simple interface to submit a recording
- **Spectrogram generation**: Automatic conversion of audio to Mel spectrogram
- **Species prediction**: Identification among classes: `Beluga`, `Dolphin`, `Orca`
- **Confidence threshold**: If prediction confidence is too low, result is classified as "Other"
- **Visualization**: Displays the generated spectrogram and prediction result

### Technologies

- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow / Keras
- **Audio Processing**: Librosa
- **Frontend**: HTML, CSS, JavaScript (with Fetch API)

---

## Français

ORCA est un projet de bioacoustique qui utilise l'intelligence artificielle pour identifier des espèces de cétacés (orques, dauphins, bélugas) à partir d'enregistrements audio sous-marins.

## 🎯 Objectif

L'application web permet d'uploader un fichier audio (`.mp3`, `.wav`) et utilise un modèle de Deep Learning (CNN) pour prédire l'espèce la plus probable présente dans l'enregistrement.

## ✨ Fonctionnalités

- **Upload de fichier audio** : Interface simple pour soumettre un enregistrement.
- **Génération de spectrogramme** : Conversion automatique de l'audio en spectrogramme Mel.
- **Prédiction d'espèce** : Identification parmi les classes : `Béluga`, `Dauphin`, `Orque`.
- **Seuil de confiance** : Si la confiance de la prédiction est trop faible, le résultat est classé comme "Autres".
- **Visualisation** : Affiche le spectrogramme généré et le résultat de la prédiction.

## 🛠️ Technologies utilisées

- **Backend** : Flask (Python)
- **Machine Learning** : TensorFlow / Keras
- **Traitement Audio** : Librosa
- **Frontend** : HTML, CSS, JavaScript (avec Fetch API)

## 📂 Structure du projet

```text
O.R.C.A/
├── app/
│   ├── static/
│   │   ├── spectrograms/   # Spectrogrammes générés par l'app (gitignored)
│   │   └── js/
│   │       └── app.js
│   ├── templates/
│   │   └── index.html
│   └── main.py           # Application Flask principale
├── models/
│   └── modele_orca.keras   # Le modèle entraîné (gitignored)
├── scripts/
│   ├── 1_generate_spectrograms.py
│   ├── 2_create_annotations.py
│   ├── 3_prepare_dataset.py
│   └── 4_train_model.py
├── tests/
│   └── test_prediction.py
├── uploads/                # Fichiers audio uploadés (gitignored)
├── requirements.txt        # Dépendances Python
└── README.md               # Ce fichier
```

## 🚀 Installation et Lancement

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/AlexandreGoss/O.R.C.A.git
    cd O.R.C.A
    ```

2.  **Créez un environnement virtuel et installez les dépendances :**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Téléchargez le modèle :**
    Vous devez avoir un fichier `modele_orca.keras` à la racine. Assurez-vous de l'avoir entraîné ou téléchargez-le si vous l'avez hébergé ailleurs.

4.  **Lancez l'application :**
    ```bash
    flask run
    ```
    Ouvrez votre navigateur et allez à `http://127.0.0.1:5000`.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` for plus de détails.