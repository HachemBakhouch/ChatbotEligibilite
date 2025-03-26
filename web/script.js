document.addEventListener('DOMContentLoaded', function () {
    // Éléments du DOM
    const chatMessages = document.getElementById('chat-messages');
    const textInput = document.getElementById('text-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const recordingIndicator = document.getElementById('recording-indicator');
    const recordingTime = document.getElementById('recording-time');
    const generatePdfButton = document.getElementById('generate-pdf-button');

    // Variables pour la conversation
    let conversationId = null;
    let conversationFinished = false;

    // Variables pour l'enregistrement audio
    let mediaRecorder = null;
    let audioChunks = [];
    let recordingInterval = null;
    let recordingSeconds = 0;
    const MAX_RECORDING_TIME = 60; // 60 secondes maximum

    // Variables pour la synthèse vocale
    let currentlySpeaking = false;
    let speechQueue = [];

    // API URL
    const API_BASE_URL = 'http://localhost:5001'; // ou 'http://127.0.0.1:5001'

    // Initialisation de la conversation
    function initConversation() {
        fetch(`${API_BASE_URL}/conversation`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors', // Spécifier explicitement le mode CORS
            body: JSON.stringify({ user_id: 'web-user-' + Date.now() })
        })
            .then(response => response.json())
            .then(data => {
                conversationId = data.conversation_id;
                addBotMessage(data.message);  // Remplacer addMessage par addBotMessage
            })
            .catch(error => {
                console.error('Error starting conversation:', error);
                addBotMessage('Erreur lors de l\'initialisation de la conversation. Veuillez réessayer.');  // Remplacer addMessage par addBotMessage
            });
    }
    // Fonction pour ajouter un message du demandeur au chat
    function addUserMessage(text, transcription = null, audioUrl = null) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', 'user-container');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'user-message');
        messageDiv.textContent = text;

        // Transcription in a separate rectangle
        if (transcription) {
            const transcriptionContainer = document.createElement('div');
            transcriptionContainer.classList.add('transcription-container');

            const transcriptionDiv = document.createElement('div');
            transcriptionDiv.classList.add('transcription');
            transcriptionDiv.textContent = transcription;

            transcriptionContainer.appendChild(transcriptionDiv);
            messageDiv.appendChild(transcriptionContainer);
        }

        // Audio in a separate rectangle
        if (audioUrl) {
            const audioContainer = document.createElement('div');
            audioContainer.classList.add('audio-message-container');

            const audioPlayer = document.createElement('audio');
            audioPlayer.src = audioUrl;

            const playButton = document.createElement('button');
            playButton.classList.add('audio-play-btn');
            playButton.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="12" fill="#3720BC"/>
                    <path d="M9 16.5V7.5L16 12L9 16.5Z" fill="white"/>
                </svg>
            `;

            playButton.addEventListener('click', () => {
                if (audioPlayer.paused) {
                    audioPlayer.play();
                    playButton.classList.add('playing');
                } else {
                    audioPlayer.pause();
                    playButton.classList.remove('playing');
                }
            });

            audioPlayer.addEventListener('ended', () => {
                playButton.classList.remove('playing');
            });

            audioContainer.appendChild(playButton);
            audioContainer.appendChild(audioPlayer);
            messageDiv.appendChild(audioContainer);
        }

        messageContainer.appendChild(messageDiv);
        chatMessages.appendChild(messageContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Fonction pour ajouter un message du chatbot au chat
    function addBotMessage(text) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container');

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

    // Fonction pour envoyer un message texte
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

                // Activer le bouton de génération PDF si la conversation est terminée
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

    // Fonction pour gérer l'enregistrement audio
    function toggleRecording() {
        if (!mediaRecorder) {
            startRecording();
        } else {
            stopRecording();
        }
    }

    // Démarrer l'enregistrement audio
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
                    // Arrêter toutes les pistes du stream
                    stream.getTracks().forEach(track => track.stop());
                };

                // Démarrer l'enregistrement
                mediaRecorder.start();
                micButton.classList.add('recording');
                recordingIndicator.style.display = 'block';

                // Afficher le temps d'enregistrement
                recordingSeconds = 0;
                recordingInterval = setInterval(() => {
                    recordingSeconds++;
                    recordingTime.textContent = recordingSeconds;

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

    // Arrêter l'enregistrement audio
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            clearInterval(recordingInterval);
            micButton.classList.remove('recording');
            recordingIndicator.style.display = 'none';
            mediaRecorder = null;
        }
    }

    // Envoyer l'audio au serveur
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

            addUserMessage('🎤 Message vocal envoyé');

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
                        // Mettre à jour le message utilisateur avec la transcription
                        const lastMessageContainer = chatMessages.lastElementChild;
                        const userMessageDiv = lastMessageContainer.querySelector('.user-message');
                        userMessageDiv.textContent = data.transcription;
                    }

                    const speakingIndicator = addBotMessage(data.message);
                    speakText(data.message, speakingIndicator);

                    // Activer le bouton de génération PDF si la conversation est terminée
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

    // Fonction pour la synthèse vocale de la réponse
    function speakText(text, speakingIndicator = null) {
        if ('speechSynthesis' in window) {
            // Ajouter à la file d'attente
            speechQueue.push({ text, speakingIndicator });

            // Si rien n'est en cours de lecture, démarrer la lecture
            if (!currentlySpeaking) {
                processNextSpeech();
            }
        }
    }

    // Traiter la prochaine synthèse vocale dans la file d'attente
    function processNextSpeech() {
        if (speechQueue.length === 0) {
            currentlySpeaking = false;
            return;
        }

        currentlySpeaking = true;
        const { text, speakingIndicator } = speechQueue.shift();

        // Afficher l'indicateur de parole
        if (speakingIndicator) {
            speakingIndicator.style.display = 'inline-block';
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'fr-FR';

        utterance.onend = function () {
            // Masquer l'indicateur de parole
            if (speakingIndicator) {
                speakingIndicator.style.display = 'none';
            }

            // Traiter la prochaine synthèse vocale
            processNextSpeech();
        };

        speechSynthesis.speak(utterance);
    }

    // Fonction pour générer le PDF
    function generatePDF() {
        if (!conversationId || !conversationFinished) {
            alert('La conversation n\'est pas terminée ou non initialisée.');
            return;
        }

        // Désactiver le bouton pendant la génération
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
                    // Ouvrir le PDF dans un nouvel onglet
                    window.open(data.file_url, '_blank');
                } else {
                    addBotMessage('Le PDF a été généré avec succès. Vous pouvez le télécharger depuis votre espace personnel.');
                }

                // Réactiver le bouton
                generatePdfButton.disabled = false;
                generatePdfButton.textContent = 'Générer PDF';
            })
            .catch(error => {
                console.error('Error generating PDF:', error);
                addBotMessage('Erreur lors de la génération du PDF. Veuillez réessayer.');

                // Réactiver le bouton
                generatePdfButton.disabled = false;
                generatePdfButton.textContent = 'Générer PDF';
            });
    }

    // Event listeners
    sendButton.addEventListener('click', sendTextMessage);
    textInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendTextMessage();
        }
    });
    micButton.addEventListener('click', toggleRecording);
    generatePdfButton.addEventListener('click', generatePDF);

    // Initialiser la conversation au chargement
    initConversation();
});