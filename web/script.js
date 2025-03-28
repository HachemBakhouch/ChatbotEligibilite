document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const textInput = document.getElementById('text-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const recordingContainer = document.getElementById('recording-container');
    const recordingPauseBtn = document.querySelector('.recording-pause-btn');
    const generatePdfButton = document.getElementById('generate-pdf-button');

    // Conversation Variables
    let conversationId = null;
    let conversationFinished = false;

    // Audio Recording Variables
    let mediaRecorder = null;
    let audioChunks = [];
    let recordingInterval = null;
    let recordingSeconds = 0;
    const MAX_RECORDING_TIME = 60; // 60 seconds maximum

    // Voice Synthesis Variables
    let currentlySpeaking = false;
    let speechQueue = [];

    // API URL
    const API_BASE_URL = 'http://localhost:5001';

    // Conversation Initialization
    function initConversation() {
        fetch(`${API_BASE_URL}/conversation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            body: JSON.stringify({ user_id: 'web-user-' + Date.now() })
        })
            .then(response => response.json())
            .then(data => {
                conversationId = data.conversation_id;
                addBotMessage(data.message);
            })
            .catch(error => {
                console.error('Error starting conversation:', error);
                addBotMessage('Erreur lors de l\'initialisation de la conversation. Veuillez réessayer.');
            });
    }

    // Start Recording
    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    sendAudioMessage(audioBlob);
                    // Stop all stream tracks
                    stream.getTracks().forEach(track => track.stop());
                };

                // Start recording
                mediaRecorder.start();
                micButton.classList.add('recording');

                // Show recording container
                recordingContainer.style.display = 'flex';

                // Recording timer
                recordingSeconds = 0;
                recordingInterval = setInterval(() => {
                    recordingSeconds++;
                    if (recordingSeconds >= MAX_RECORDING_TIME) {
                        stopRecording();
                    }
                }, 1000);
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                alert('Impossible d\'accéder au microphone. Veuillez vérifier les permissions.');
            });
    }

    // Stop Recording
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            clearInterval(recordingInterval);
            micButton.classList.remove('recording');

            // Hide recording container
            recordingContainer.style.display = 'none';

            mediaRecorder = null;
        }
    }

    // Send Audio Message
    // Send Audio Message
    // Mettre à jour la fonction sendAudioMessage pour créer correctement le message audio
    function sendAudioMessage(audioBlob) {
        if (!conversationId) {
            addBotMessage('Conversation non initialisée. Veuillez attendre...');
            return;
        }

        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            // Format base64: data:audio/wav;base64,XXXXXX
            const base64Audio = reader.result.split(',')[1];

            // Créer URL pour l'audio
            const audioUrl = URL.createObjectURL(audioBlob);

            // Ajouter un message temporaire en attendant la transcription
            addUserMessage('🎤 Message vocal envoyé', null, audioUrl);

            fetch(`${API_BASE_URL}/process-audio`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                body: JSON.stringify({
                    conversation_id: conversationId,
                    audio: base64Audio
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.transcription) {
                        // Supprimer le message temporaire
                        chatMessages.removeChild(chatMessages.lastElementChild);

                        // Ajouter un nouveau message avec la transcription et l'audio
                        addUserMessage(data.transcription, null, audioUrl);
                    }

                    // Slight delay before adding bot message
                    setTimeout(() => {
                        const speakingIndicator = addBotMessage(data.message);
                        speakText(data.message, speakingIndicator);
                    }, 500);

                    // Activate PDF generation if conversation is finished
                    if (data.is_final) {
                        conversationFinished = true;
                        generatePdfButton.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Error sending audio message:', error);
                    addBotMessage('Erreur lors de l\'envoi du message audio. Veuillez réessayer.');
                });
        };
    }

    // Mettre à jour cette fonction pour afficher correctement les messages audio
    function addUserMessage(text, transcription = null, audioUrl = null) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', 'user-container');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user-message');
        messageDiv.textContent = text;

        // Si un message a été enregistré via l'audio
        if (audioUrl) {
            console.log("Creating audio container with URL:", audioUrl); // Débogage

            // Créer container pour audio player
            const audioContainer = document.createElement('div');
            audioContainer.classList.add('audio-message-container');

            // Créer bouton play
            const playButton = document.createElement('button');
            playButton.classList.add('audio-play-btn');
            playButton.innerHTML = `
             <svg width="24" height="24" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="14" cy="14" r="12" fill="#FFFFFF"/>
                <path d="M11 18V10L19 14L11 18Z" fill="#3720BC"/>
            </svg>
        `;

            // Créer waveform
            const waveformDiv = document.createElement('div');
            waveformDiv.classList.add('audio-waveform');
            const waveformImg = document.createElement('img');
            waveformImg.src = '/assets/waveform1.png';
            waveformImg.alt = 'Audio Waveform';
            waveformDiv.appendChild(waveformImg);

            // Créer timer
            const timerDiv = document.createElement('div');
            timerDiv.classList.add('audio-timer');
            timerDiv.textContent = '0:00';

            // Créer icône volume
            const volumeDiv = document.createElement('div');
            volumeDiv.classList.add('audio-volume');
            const volumeImg = document.createElement('img');
            volumeImg.src = '/assets/volume.png';
            volumeImg.alt = 'Volume';
            volumeDiv.appendChild(volumeImg);

            // Créer element audio caché
            const audioElement = document.createElement('audio');
            audioElement.src = audioUrl;
            audioElement.style.display = 'none';

            // Ajouter les éléments au container
            audioContainer.appendChild(playButton);
            audioContainer.appendChild(waveformDiv);
            audioContainer.appendChild(timerDiv);
            audioContainer.appendChild(volumeDiv);
            audioContainer.appendChild(audioElement);

            // Ajouter événements pour le bouton play
            let isPlaying = false;
            let timer = null;
            let seconds = 0;

            playButton.addEventListener('click', () => {
                if (!isPlaying) {
                    audioElement.play();
                    isPlaying = true;

                    // Démarrer le timer
                    seconds = 0;
                    timerDiv.textContent = '0:00';
                    timer = setInterval(() => {
                        seconds++;
                        const mins = Math.floor(seconds / 60);
                        const secs = String(seconds % 60).padStart(2, '0');
                        timerDiv.textContent = `${mins}:${secs}`;
                    }, 1000);
                } else {
                    audioElement.pause();
                    isPlaying = false;

                    // Arrêter le timer
                    clearInterval(timer);
                }
            });

            audioElement.addEventListener('ended', () => {
                isPlaying = false;
                clearInterval(timer);
                timerDiv.textContent = '0:00';
            });

            // Si transcription fournie, l'ajouter comme texte séparé au-dessus du lecteur audio
            if (transcription) {
                const transcriptionDiv = document.createElement('div');
                transcriptionDiv.classList.add('transcription-container');
                transcriptionDiv.textContent = transcription;
                messageDiv.appendChild(transcriptionDiv);
            }

            // Ajouter le player audio
            messageDiv.appendChild(audioContainer);
        }

        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add User Message
    // Mettre à jour cette fonction dans script.js
    // Fonction modifiée pour séparer le texte transcrit et l'audio en deux conteneurs distincts
    function addUserMessage(text, transcription = null, audioUrl = null) {
        // Créer le conteneur principal de message utilisateur
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', 'user-container');

        // Créer et ajouter le message texte principal
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user-message');
        messageDiv.textContent = text;
        messageContainer.appendChild(messageDiv);

        // Si une transcription est fournie, l'ajouter comme un conteneur distinct
        if (transcription) {
            const transcriptionContainer = document.createElement('div');
            transcriptionContainer.classList.add('message-container', 'user-container');

            const transcriptionDiv = document.createElement('div');
            transcriptionDiv.classList.add('message', 'user-transcription');
            transcriptionDiv.textContent = transcription;

            transcriptionContainer.appendChild(transcriptionDiv);
            chatMessages.appendChild(transcriptionContainer);
        }

        // Si un URL audio est fourni, créer un conteneur audio distinct
        if (audioUrl) {
            console.log("Creating separate audio container with URL:", audioUrl);

            const audioContainer = document.createElement('div');
            audioContainer.classList.add('message-container', 'user-container');

            const audioPlayerDiv = document.createElement('div');
            audioPlayerDiv.classList.add('audio-message-container');

            // Créer bouton play
            const playButton = document.createElement('button');
            playButton.classList.add('audio-play-btn');
            playButton.innerHTML = `
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="14" cy="14" r="14" fill="#FFFFFF"/>
                <path d="M10 19V9L20 14L10 19Z" fill="#3720BC"/>
            </svg>
        `;

            // Créer waveform
            const waveformDiv = document.createElement('div');
            waveformDiv.classList.add('audio-waveform');
            const waveformImg = document.createElement('img');
            waveformImg.src = '/assets/waveform1.png';
            waveformImg.alt = 'Audio Waveform';
            waveformDiv.appendChild(waveformImg);

            // Créer timer
            const timerDiv = document.createElement('div');
            timerDiv.classList.add('audio-timer');
            timerDiv.textContent = '0:00';

            // Créer icône volume
            const volumeDiv = document.createElement('div');
            volumeDiv.classList.add('audio-volume');
            const volumeImg = document.createElement('img');
            volumeImg.src = '/assets/volume.png';
            volumeImg.alt = 'Volume';
            volumeDiv.appendChild(volumeImg);

            // Créer element audio caché
            const audioElement = document.createElement('audio');
            audioElement.src = audioUrl;
            audioElement.style.display = 'none';

            // Ajouter les éléments au container audio
            audioPlayerDiv.appendChild(playButton);
            audioPlayerDiv.appendChild(waveformDiv);
            audioPlayerDiv.appendChild(timerDiv);
            audioPlayerDiv.appendChild(volumeDiv);
            audioPlayerDiv.appendChild(audioElement);

            // Ajouter le player audio au conteneur
            audioContainer.appendChild(audioPlayerDiv);

            // Ajouter événements pour le bouton play
            let isPlaying = false;
            let timer = null;
            let seconds = 0;

            playButton.addEventListener('click', () => {
                if (!isPlaying) {
                    audioElement.play();
                    isPlaying = true;

                    // Démarrer le timer
                    seconds = 0;
                    timerDiv.textContent = '0:00';
                    timer = setInterval(() => {
                        seconds++;
                        const mins = Math.floor(seconds / 60);
                        const secs = String(seconds % 60).padStart(2, '0');
                        timerDiv.textContent = `${mins}:${secs}`;
                    }, 1000);
                } else {
                    audioElement.pause();
                    isPlaying = false;

                    // Arrêter le timer
                    clearInterval(timer);
                }
            });

            audioElement.addEventListener('ended', () => {
                isPlaying = false;
                clearInterval(timer);
                timerDiv.textContent = '0:00';
            });

            // Ajouter le conteneur audio au chat
            chatMessages.appendChild(audioContainer);
        }

        // Ajouter le conteneur de message principal au chat
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Mise à jour de la fonction sendAudioMessage pour utiliser les nouveaux conteneurs séparés
    function sendAudioMessage(audioBlob) {
        if (!conversationId) {
            addBotMessage('Conversation non initialisée. Veuillez attendre...');
            return;
        }

        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
            // Format base64: data:audio/wav;base64,XXXXXX
            const base64Audio = reader.result.split(',')[1];

            // Créer URL pour l'audio
            const audioUrl = URL.createObjectURL(audioBlob);

            // Ajouter un message temporaire en attendant la transcription
            addUserMessage('🎤 Message vocal envoyé', null, audioUrl);

            fetch(`${API_BASE_URL}/process-audio`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                mode: 'cors',
                body: JSON.stringify({
                    conversation_id: conversationId,
                    audio: base64Audio
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.transcription) {
                        // Supprimer les messages temporaires (message et audio)
                        chatMessages.removeChild(chatMessages.lastElementChild); // Audio container
                        chatMessages.removeChild(chatMessages.lastElementChild); // Message container

                        // Ajouter un nouveau message avec la transcription comme message principal
                        addUserMessage(data.transcription, null, audioUrl);
                    }

                    // Slight delay before adding bot message
                    setTimeout(() => {
                        const speakingIndicator = addBotMessage(data.message);
                        speakText(data.message, speakingIndicator);
                    }, 500);

                    // Activate PDF generation if conversation is finished
                    if (data.is_final) {
                        conversationFinished = true;
                        generatePdfButton.disabled = false;
                    }
                })
                .catch(error => {
                    console.error('Error sending audio message:', error);
                    addBotMessage('Erreur lors de l\'envoi du message audio. Veuillez réessayer.');
                });
        };
    }

    // Add Bot Message
    function addBotMessage(text) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', 'bot-container');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');
        messageDiv.textContent = text;

        // Speaking Indicator
        const speakingIndicator = document.createElement('span');
        speakingIndicator.classList.add('speaking-indicator');
        speakingIndicator.style.display = 'none';
        messageDiv.appendChild(speakingIndicator);

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('message-avatar', 'bot-avatar');

        // Create robot image
        const robotImg = document.createElement('img');
        robotImg.src = '/assets/robot-icon.png';
        robotImg.alt = 'Robot Assistant';
        robotImg.classList.add('robot-avatar-icon');

        avatarDiv.appendChild(robotImg);

        messageContainer.appendChild(avatarDiv);
        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        return speakingIndicator;
    }

    // Send Text Message
    function sendTextMessage() {
        const text = textInput.value.trim();
        if (!text) return;

        addUserMessage(text);
        textInput.value = '';

        if (!conversationId) {
            addBotMessage('Conversation non initialisée. Veuillez attendre...');
            return;
        }

        fetch(`${API_BASE_URL}/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            body: JSON.stringify({
                conversation_id: conversationId,
                text: text
            })
        })
            .then(response => response.json())
            .then(data => {
                const speakingIndicator = addBotMessage(data.message);
                speakText(data.message, speakingIndicator);

                // Activate PDF generation if conversation is finished
                if (data.is_final) {
                    conversationFinished = true;
                    generatePdfButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
                addBotMessage('Erreur lors de l\'envoi du message. Veuillez réessayer.');
            });
    }

    // Speak Text
    function speakText(text, speakingIndicator = null) {
        if ('speechSynthesis' in window) {
            speechQueue.push({ text, speakingIndicator });

            if (!currentlySpeaking) {
                processNextSpeech();
            }
        }
    }

    // Process Next Speech
    function processNextSpeech() {
        if (speechQueue.length === 0) {
            currentlySpeaking = false;
            return;
        }

        currentlySpeaking = true;
        const { text, speakingIndicator } = speechQueue.shift();

        if (speakingIndicator) {
            speakingIndicator.style.display = 'inline-block';
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'fr-FR';

        utterance.onend = function () {
            if (speakingIndicator) {
                speakingIndicator.style.display = 'none';
            }

            processNextSpeech();
        };

        speechSynthesis.speak(utterance);
    }

    // Generate PDF
    function generatePDF() {
        if (!conversationId || !conversationFinished) {
            alert('La conversation n\'est pas terminée ou non initialisée.');
            return;
        }

        generatePdfButton.disabled = true;
        generatePdfButton.textContent = 'Génération en cours...';

        fetch(`${API_BASE_URL}/generate-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            body: JSON.stringify({
                conversation_id: conversationId
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.file_url) {
                    window.open(data.file_url, '_blank');
                } else {
                    addBotMessage('Le PDF a été généré avec succès. Vous pouvez le télécharger depuis votre espace personnel.');
                }

                generatePdfButton.disabled = false;
                generatePdfButton.textContent = 'Générer PDF';
            })
            .catch(error => {
                console.error('Error generating PDF:', error);
                addBotMessage('Erreur lors de la génération du PDF. Veuillez réessayer.');

                generatePdfButton.disabled = false;
                generatePdfButton.textContent = 'Générer PDF';
            });
    }

    // Event Listeners
    sendButton.addEventListener('click', sendTextMessage);
    textInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendTextMessage();
        }
    });
    micButton.addEventListener('click', startRecording);
    recordingPauseBtn.addEventListener('click', stopRecording);
    generatePdfButton.addEventListener('click', generatePDF);

    // Initialize Conversation
    initConversation();
});