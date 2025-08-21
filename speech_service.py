"""
Service for interacting with the Speech API.
"""

import os
import logging
import requests
from typing import Dict, List, Any, Optional
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SpeechService:
    """
    Service for interacting with the Speech API.
    """
    
    def __init__(self, api_url: str = None):
        """
        Initialize the speech service.
        
        Args:
            api_url: URL of the Speech API
        """
        self.api_url = api_url or os.environ.get("SPEECH_API_URL", "http://localhost:3003/api")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the Speech API.
        
        Returns:
            Health status
        """
        try:
            response = requests.get(f"{self.api_url}/speech/health")
            
            if response.status_code == 200:
                return {
                    "status": "ok",
                    "details": response.json()
                }
            else:
                return {
                    "status": "error",
                    "details": {
                        "status_code": response.status_code,
                        "message": response.text
                    }
                }
        except Exception as e:
            logger.exception("Error checking Speech API health")
            return {
                "status": "error",
                "details": {
                    "message": str(e)
                }
            }
    
    def speech_to_text(self, audio_file_path: str, language_code: str = "en-US") -> Dict[str, Any]:
        """
        Convert speech to text.
        
        Args:
            audio_file_path: Path to the audio file
            language_code: Language code
            
        Returns:
            Transcription result
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                files = {
                    "audio": (os.path.basename(audio_file_path), audio_file, "audio/wav")
                }
                
                data = {
                    "language_code": language_code
                }
                
                response = requests.post(
                    f"{self.api_url}/speech/stt",
                    files=files,
                    data=data
                )
                
                if response.status_code == 200:
                    return {
                        "status": "ok",
                        "result": response.json()
                    }
                else:
                    return {
                        "status": "error",
                        "details": {
                            "status_code": response.status_code,
                            "message": response.text
                        }
                    }
        except Exception as e:
            logger.exception("Error converting speech to text")
            return {
                "status": "error",
                "details": {
                    "message": str(e)
                }
            }
    
    def text_to_speech(
        self,
        text: str,
        language_code: str = "en-US",
        voice_name: str = "en-US-Neural2-F",
        output_file_path: str = None
    ) -> Dict[str, Any]:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            language_code: Language code
            voice_name: Voice name
            output_file_path: Path to save the audio file (optional)
            
        Returns:
            Path to the generated audio file
        """
        try:
            data = {
                "text": text,
                "language_code": language_code,
                "voice_name": voice_name
            }
            
            response = requests.post(
                f"{self.api_url}/speech/tts",
                json=data
            )
            
            if response.status_code == 200:
                # Save the audio to a file
                if not output_file_path:
                    output_file_path = tempfile.mktemp(suffix=".mp3")
                
                with open(output_file_path, "wb") as f:
                    f.write(response.content)
                
                return {
                    "status": "ok",
                    "file_path": output_file_path
                }
            else:
                return {
                    "status": "error",
                    "details": {
                        "status_code": response.status_code,
                        "message": response.text
                    }
                }
        except Exception as e:
            logger.exception("Error converting text to speech")
            return {
                "status": "error",
                "details": {
                    "message": str(e)
                }
            }
    
    def speech_to_text_to_speech(
        self,
        audio_file_path: str,
        stt_language_code: str = "en-US",
        tts_language_code: str = "en-US",
        tts_voice_name: str = "en-US-Neural2-F",
        output_file_path: str = None
    ) -> Dict[str, Any]:
        """
        Convert speech to text, then text to speech.
        
        Args:
            audio_file_path: Path to the audio file
            stt_language_code: Language code for speech-to-text
            tts_language_code: Language code for text-to-speech
            tts_voice_name: Voice name for text-to-speech
            output_file_path: Path to save the audio file (optional)
            
        Returns:
            Path to the generated audio file and transcription
        """
        try:
            # First, convert speech to text
            stt_result = self.speech_to_text(audio_file_path, stt_language_code)
            
            if stt_result["status"] != "ok":
                return stt_result
            
            # Extract the transcription
            transcription = stt_result["result"]["results"][0]["transcript"]
            
            # Then, convert text to speech
            tts_result = self.text_to_speech(
                transcription,
                tts_language_code,
                tts_voice_name,
                output_file_path
            )
            
            if tts_result["status"] != "ok":
                return tts_result
            
            return {
                "status": "ok",
                "file_path": tts_result["file_path"],
                "transcription": transcription
            }
        except Exception as e:
            logger.exception("Error in speech-to-text-to-speech")
            return {
                "status": "error",
                "details": {
                    "message": str(e)
                }
            }
    
    def list_voices(self, language_code: str = None) -> Dict[str, Any]:
        """
        List available voices for text-to-speech.
        
        Args:
            language_code: Language code to filter voices
            
        Returns:
            List of available voices
        """
        try:
            params = {}
            if language_code:
                params["language_code"] = language_code
            
            response = requests.get(
                f"{self.api_url}/speech/tts/voices",
                params=params
            )
            
            if response.status_code == 200:
                return {
                    "status": "ok",
                    "voices": response.json().get("voices", [])
                }
            else:
                return {
                    "status": "error",
                    "details": {
                        "status_code": response.status_code,
                        "message": response.text
                    }
                }
        except Exception as e:
            logger.exception("Error listing voices")
            return {
                "status": "error",
                "details": {
                    "message": str(e)
                }
            }

