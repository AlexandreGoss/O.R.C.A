import librosa
import librosa.display
# import matplotlib
# matplotlib.use('TkAgg')  # Utilise le backend interactif
import matplotlib.pyplot as plt
import numpy as np



def audio_to_spectrogram(file_path, save_image=False):
    # Charger l'audio
    audio, sr = librosa.load(file_path, sr=None)
    # Calculer le spectrogramme (Mél spectrogramme)
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128, fmax=8000)
    log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    
    # Afficher le spectrogramme
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(log_spectrogram, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    if save_image:
        plt.savefig('dolphtest1.png')
    plt.show()
    
    return log_spectrogram

audio_to_spectrogram('/home/alexandre/Documents/ProjetO.R.C.A/audioCetaces/belugatest1.mp3', save_image=True)