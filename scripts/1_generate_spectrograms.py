import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Dossier contenant les fichiers audio
AUDIO_DIR = "audioCetaces"
# Dossier où seront enregistrés les spectrogrammes
OUTPUT_DIR = "spectrograms"

# S'assurer que le dossier de sortie existe
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_spectrogram(file_path, output_path):
    """Génère un spectrogramme à partir d'un fichier audio."""
    y, sr = librosa.load(file_path, sr=None)  # Charger l'audio avec le taux d'échantillonnage d'origine
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)  
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)  # Conversion en échelle logarithmique

    # Création du spectrogramme
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title(f"Spectrogramme de {os.path.basename(file_path)}")
    plt.tight_layout()

    # Sauvegarde de l'image
    plt.savefig(output_path)
    plt.close()  # Fermer la figure pour éviter une surcharge mémoire
    print(f"Spectrogramme sauvegardé : {output_path}")

# Parcours du dossier audio pour traiter chaque fichier
for subdir, _, files in os.walk(AUDIO_DIR):
    for file in files:
        if file.endswith(".mp3"):  # Vérifier que c'est bien un fichier audio
            file_path = os.path.join(subdir, file)
            output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file)[0]}.png")
            generate_spectrogram(file_path, output_path)
