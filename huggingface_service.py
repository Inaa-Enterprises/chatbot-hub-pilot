"""
Hugging Face service for generating AI responses.
This service uses the free Hugging Face Inference API.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, AsyncGenerator, Optional

logger = logging.getLogger(__name__)

# Configuration
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models"
DEFAULT_MODEL = "microsoft/DialoGPT-large"  # A free conversational model

class HuggingFaceService:
    """Handles interactions with the Hugging Face Inference API."""
    
    def __init__(self):
        self.api_key = HUGGING_FACE_API_KEY
        self.default_model = DEFAULT_MODEL
        
        if not self.api_key:
            logger.warning("HUGGING_FACE_API_KEY not set. Hugging Face service will not work.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_response(self, system_instruction: str, message: str, model: str = None) -> str:
        """
        Generate a response using Hugging Face models.
        
        Args:
            system_instruction: System prompt or instruction
            message: User message
            model: Specific model to use (optional)
            
        Returns:
            Generated response text
        """
        if not self.api_key:
            return "Hugging Face API key not configured. Please set HUGGING_FACE_API_KEY environment variable."
        
        model = model or self.default_model
        
        # Format the input for conversational models
        inputs = f"{system_instruction}\nUser: {message}\nAI:"
        
        payload = {
            "inputs": inputs,
            "parameters": {
                "max_new_tokens": 200,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"{HUGGING_FACE_API_URL}/{model}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                else:
                    return str(result)
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return f"Error generating response: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error during Hugging Face API call: {e}")
            return f"Error generating response: {str(e)}"
    
    def list_available_models(self) -> List[str]:
        """
        List some popular free models available on Hugging Face.
        """
        return [
            "microsoft/DialoGPT-large",
            "facebook/blenderbot-400M-distill",
            "microsoft/DialoGPT-medium",
            "google/flan-t5-base",
            "google/flan-t5-small",
            "gpt2"
        ]
    
    def generate_with_model(self, model: str, prompt: str) -> str:
        """
        Generate a response using a specific model.
        
        Args:
            model: Model identifier
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        if not self.api_key:
            return "Hugging Face API key not configured."
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(
                f"{HUGGING_FACE_API_URL}/{model}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                else:
                    return str(result)
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return f"Error: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error during Hugging Face API call: {e}")
            return f"Error: {str(e)}"

# For backwards compatibility
AIService = HuggingFaceService