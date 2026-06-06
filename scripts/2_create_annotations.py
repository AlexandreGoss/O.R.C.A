import os
import csv

# Dossier contenant les fichiers audio
AUDIO_DIR = "audioCetaces"
# Dossier des spectrogrammes
SPECTROGRAM_DIR = "spectrograms"
# Nom du fichier CSV de sortie
CSV_FILE = "labels.csv"

# Ouvrir le fichier CSV en mode écriture
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["file_name", "label"])  # Écrire l'en-tête

    # Parcours des fichiers audio classés par espèce
    for subdir, _, files in os.walk(AUDIO_DIR):
        label = os.path.basename(subdir)  # Nom du dossier = label

        for file in files:
            if file.endswith(".mp3"):  # Vérifier que c'est un fichier audio
                spectrogram_name = f"{os.path.splitext(file)[0]}.png"  # Convertir en nom d'image
                spectrogram_path = os.path.join(SPECTROGRAM_DIR, spectrogram_name)

                # Vérifier si le spectrogramme correspondant existe
                if os.path.exists(spectrogram_path):
                    writer.writerow([spectrogram_name, label])
                    print(f"Ajouté : {spectrogram_name} → {label}")
                else:
                    print(f"⚠️ Spectrogramme introuvable pour {file}")

print(f"✅ Fichier {CSV_FILE} généré avec succès !")
