import requests
import base64
import json
import os
import tempfile


class WhisperAdapter:
    """Adapter for OpenAI's Whisper API"""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/audio/transcriptions"

    def transcribe(self, audio_data, language="fr"):
        """
        Transcribe audio data using OpenAI's Whisper API

        Args:
            audio_data (str): Base64-encoded audio data
            language (str): Language code (default: 'fr')

        Returns:
            str: Transcribed text
        """
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)

            # Create a temporary file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(audio_bytes)

            # Prepare the request
            headers = {"Authorization": f"Bearer {self.api_key}"}

            with open(temp_filename, "rb") as audio_file:
                files = {
                    "file": audio_file,
                    "model": (None, "whisper-1"),
                    "language": (None, language),
                }

                response = requests.post(self.api_url, headers=headers, files=files)

            # Clean up the temporary file
            os.unlink(temp_filename)

            # Process the response
            if response.status_code == 200:
                return response.json().get("text", "")
            else:
                raise Exception(f"API error: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
