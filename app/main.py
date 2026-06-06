import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template, url_for
import tensorflow as tf
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
# En supposant que l'application est lancée depuis la racine du projet
UPLOAD_FOLDER = "uploads"
SPECTROGRAM_FOLDER = "app/static/spectrograms"  # Chemin sur le disque pour la sauvegarde
MODEL_PATH = "models/modele_orca.keras"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assurez-vous que les dossiers existent
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(SPECTROGRAM_FOLDER, exist_ok=True)

# Charger le modèle
model = tf.keras.models.load_model(MODEL_PATH)

# Classes cétacés
class_names = ["Beluga", "Dauphin", "Orque"]
ALLOWED_EXTENSIONS = {"wav", "mp3"}

def generate_spectrogram(file_path, output_path):
    """Génère un spectrogramme Mel et le sauvegarde en PNG."""
    y, sr = librosa.load(file_path, sr=None)  # Charge l’audio en conservant son taux d’échantillonnage
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

    # Création de la figure
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogramme")
    plt.tight_layout()

    # Sauvegarde
    plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nom de fichier invalide"}), 400
    
    if not (file and allowed_file(file.filename)):
        return jsonify({"error": "Format de fichier non supporté. Utilisez .mp3 ou .wav"}), 400

    # Sauvegarde temporaire du MP3
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Génération du spectrogramme
    spectro_filename = os.path.splitext(filename)[0] + ".png"
    spectro_path = os.path.join(SPECTROGRAM_FOLDER, spectro_filename)
    generate_spectrogram(file_path, spectro_path)

    # Chargement du spectrogramme pour le modèle
    img = tf.keras.preprocessing.image.load_img(spectro_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ajout d’une dimension batch

    # Prédiction
    predictions = model.predict(img_array)[0]  # Récupère le tableau de probabilités
    predicted_class = np.argmax(predictions)
    confidence = predictions[predicted_class]  # Probabilité associée à la classe prédite

    # Définition du seuil de confiance
    confidence_threshold = 0.7  # 70%

    if confidence < confidence_threshold:
        result = "Autres"
    else:
        result = class_names[predicted_class]

    return jsonify({
        "prediction": result,
        "confidence": round(float(confidence) * 100, 2),  # Converti en pourcentage
        # Génère une URL pour le fichier statique. Flask le servira depuis /static/spectrograms/...
        "spectrogram_url": url_for('static', filename=f'spectrograms/{spectro_filename}')
    })

if __name__ == "__main__":
    app.run(debug=True)