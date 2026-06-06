// Fonction pour générer un spectrogramme à partir d'un AudioBuffer
async function generateSpectrogram(audioBuffer) {
    // Paramètres du spectrogramme
    const sampleRate = audioBuffer.sampleRate;
    const channelData = audioBuffer.getChannelData(0); // Prendre le premier canal
    
    // Paramètres STFT
    const fftSize = 2048;
    const hopSize = Math.floor(fftSize / 4);
    const nFrames = Math.ceil(channelData.length / hopSize);
    
    // Créer un contexte d'analyse
    const offlineCtx = new (window.OfflineAudioContext || window.webkitOfflineAudioContext)(
        1,                      // Nombre de canaux
        channelData.length,      // Longueur de la trame
        sampleRate              // Taux d'échantillonnage
    );
    
    // Créer un nœud d'analyse
    const analyser = offlineCtx.createAnalyser();
    analyser.fftSize = fftSize;
    analyser.smoothingTimeConstant = 0;
    
    // Créer un nœud de source pour le buffer audio
    const source = offlineCtx.createBufferSource();
    source.buffer = audioBuffer;
    
    // Connecter les nœuds
    source.connect(analyser);
    analyser.connect(offlineCtx.destination);
    
    // Démarrer la lecture
    source.start(0);
    
    // Tableau pour stocker les données du spectrogramme
    const spectrogram = [];
    const freqData = new Uint8Array(analyser.frequencyBinCount);
    
    // Extraire les données de fréquence pour chaque trame
    for (let i = 0; i < nFrames; i++) {
        const startSample = i * hopSize;
        const endSample = Math.min(startSample + fftSize, channelData.length);
        
        // Créer une vue sur les données de cette trame
        const frame = channelData.slice(startSample, endSample);
        
        // Si la trame est plus petite que fftSize, la compléter avec des zéros
        if (frame.length < fftSize) {
            const paddedFrame = new Float32Array(fftSize);
            paddedFrame.set(frame);
            analyser.getFloatFrequencyData(paddedFrame);
            frame = paddedFrame;
        }
        
        // Obtenir les données de fréquence
        analyser.getByteFrequencyData(freqData);
        
        // Convertir en tableau normal et normaliser entre 0 et 1
        const frameData = Array.from(freqData).map(x => x / 255);
        spectrogram.push(frameData);
    }
    
    return spectrogram;
}

// Fonction pour dessiner le spectrogramme sur un canvas
function drawSpectrogram(canvas, spectrogram) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Effacer le canvas
    ctx.clearRect(0, 0, width, height);
    
    if (!spectrogram || spectrogram.length === 0) return;
    
    const nFrames = spectrogram.length;
    const nBins = spectrogram[0].length;
    
    // Dimensions de chaque case du spectrogramme
    const cellWidth = width / nFrames;
    const cellHeight = height / nBins;
    
    // Dessiner le spectrogramme
    for (let t = 0; t < nFrames; t++) {
        for (let f = 0; f < nBins; f++) {
            // Inverser l'axe des fréquences (les basses fréquences en bas)
            const y = height - (f + 1) * cellHeight;
            
            // Obtenir la valeur d'amplitude (0-1)
            const value = spectrogram[t][f];
            
            // Convertir en niveau de gris (0-255)
            const grayValue = Math.floor(value * 255);
            
            // Définir la couleur
            ctx.fillStyle = `rgb(${grayValue},${grayValue},${grayValue})`;
            
            // Dessiner le rectangle
            ctx.fillRect(t * cellWidth, y, cellWidth + 1, cellHeight + 1);
        }
    }
}

// Exporter les fonctions
window.audioProcessor = {
    generateSpectrogram,
    drawSpectrogram
};
