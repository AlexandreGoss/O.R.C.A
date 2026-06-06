document.addEventListener('DOMContentLoaded', () => {
    const audioInput = document.getElementById('audioInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const statusElement = document.getElementById('status');
    const predictionResult = document.getElementById('predictionResult');
    const spectrogramContainer = document.getElementById('spectrogramContainer'); // Assure-toi d'avoir un <div id="spectrogramContainer"></div> dans ton HTML

    analyzeBtn.addEventListener('click', async () => {
        if (!audioInput.files || audioInput.files.length === 0) {
            alert('Veuillez sélectionner un fichier audio.');
            return;
        }

        const file = audioInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // Réinitialiser l'interface
        statusElement.textContent = 'Analyse en cours...';
        analyzeBtn.disabled = true;
        predictionResult.innerHTML = '';
        if(spectrogramContainer) spectrogramContainer.innerHTML = '';

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erreur HTTP: ${response.status}`);
            }

            const data = await response.json();

            // Afficher les résultats
            statusElement.textContent = 'Analyse terminée !';
            
            let resultHTML = `<h3>Prédiction : ${data.prediction}</h3>`;
            resultHTML += `<p>Confiance : ${data.confidence}%</p>`;
            predictionResult.innerHTML = resultHTML;

            // Afficher le spectrogramme
            if (data.spectrogram_url && spectrogramContainer) {
                const img = document.createElement('img');
                img.src = data.spectrogram_url;
                img.alt = 'Spectrogramme généré';
                img.style.maxWidth = '100%';
                spectrogramContainer.appendChild(img);
            }

        } catch (error) {
            console.error("Erreur lors de l'analyse :", error);
            statusElement.textContent = `Erreur : ${error.message}`;
        } finally {
            analyzeBtn.disabled = false;
        }
    });
});
