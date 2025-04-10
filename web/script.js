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
    const API_BASE_URL = window.location.origin + '/api';

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
            addUserMessage('<div class="line_emoji">🎤 Message vocal envoyé</div>', null, audioUrl);

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
        console.log("Message original:", text);

        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message-container', 'bot-container');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'bot-message');

        // Méthode radicale: analyser et reconstruire tout lien trouvé
        let parts = [];

        // Expression régulière pour détecter les balises <a>
        const regex = /<a href=['"]([^'"]+)['"][^>]*>(.*?)<\/a>/gi;
        let lastIndex = 0;
        let match;

        // Diviser le texte et extraire les liens
        while ((match = regex.exec(text)) !== null) {
            // Ajouter le texte avant le lien
            if (match.index > lastIndex) {
                parts.push({
                    type: 'text',
                    content: text.substring(lastIndex, match.index)
                });
            }

            // Ajouter le lien
            parts.push({
                type: 'link',
                url: match[1],
                content: match[2]
            });

            lastIndex = regex.lastIndex;
        }

        // Ajouter le reste du texte après le dernier lien
        if (lastIndex < text.length) {
            parts.push({
                type: 'text',
                content: text.substring(lastIndex)
            });
        }

        // Si aucun lien n'est trouvé, utiliser le texte complet
        if (parts.length === 0) {
            parts.push({
                type: 'text',
                content: text
            });
        }

        console.log("Parts:", parts);

        // Construire le contenu du message avec des éléments DOM distincts
        parts.forEach(part => {
            if (part.type === 'text') {
                const textNode = document.createTextNode(part.content);
                messageDiv.appendChild(textNode);
            } else if (part.type === 'link') {
                // Créer un vrai lien DOM
                const linkElement = document.createElement('a');

                // Mettre à jour l'URL si nécessaire
                let url = part.url;
                if (url.includes('82.25.117.27')) {
                    url = url.replace('http://82.25.117.27', 'https://code93.fr');
                }

                linkElement.href = url;
                linkElement.textContent = part.content;
                linkElement.target = '_blank';
                linkElement.rel = 'noopener noreferrer';

                // Styles directs pour garantir l'apparence du lien
                linkElement.style.color = '#3720BC';
                linkElement.style.textDecoration = 'underline';
                linkElement.style.cursor = 'pointer';

                // Ajouter un gestionnaire d'événements explicite
                linkElement.addEventListener('click', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    window.open(this.href, '_blank');
                });

                messageDiv.appendChild(linkElement);
            }
        });

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

        console.log("DOM après création:", messageDiv.innerHTML);

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
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erreur réseau: ${response.status}`);
                }
                return response.json();
            })
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
                // Ne pas afficher de message d'erreur dans l'interface pour l'utilisateur
                // addBotMessage('Erreur lors de l\'envoi du message. Veuillez réessayer.');
            });
    }
    // Fonction améliorée pour nettoyer le HTML pour le text-to-speech
    function stripHtml(html) {
        // Créer un élément div temporaire hors du DOM
        const tempDiv = document.createElement('div');
        // Définir le HTML
        tempDiv.innerHTML = html;
        // Récupérer le texte
        let text = tempDiv.textContent || tempDiv.innerText || '';
        // Nettoyage supplémentaire: supprimer les espaces excessifs
        text = text.replace(/\s+/g, ' ').trim();
        return text;
    }
    // Speak Text
    function speakText(text, speakingIndicator = null) {
        if ('speechSynthesis' in window) {
            // Nettoyer le HTML et les emojis
            const cleanText = stripHtml(text);

            // Filtrer les emojis
            const textWithoutEmojis = cleanText.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '');

            console.log("Texte original:", text);
            console.log("Texte à prononcer:", textWithoutEmojis);

            speechQueue.push({ text: textWithoutEmojis, speakingIndicator });

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

        // Ajout d'une petite pause pour assurer un meilleur fonctionnement
        setTimeout(() => {
            speechSynthesis.speak(utterance);
        }, 50);
    }

    // Generate PDF
    function generatePDF() {
        console.log("Fonctionnalité de génération PDF désactivée");
        // Le reste du code commenté
        /*
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
            */
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
    /*
    generatePdfButton.addEventListener('click', generatePDF);
    */

    // Initialize Conversation
    initConversation();
});