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

            // First, add a generic audio message
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
                        // Update the last user message with transcription
                        const lastMessageContainer = chatMessages.lastElementChild;
                        const userMessageDiv = lastMessageContainer.querySelector('.user-message');
                        userMessageDiv.textContent = data.transcription;
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

    // Add User Message
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