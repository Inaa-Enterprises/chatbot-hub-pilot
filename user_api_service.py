"""
User API service that allows users to provide their own API keys.
This service enables users to use their own Hugging Face API keys without 
having to set environment variables during deployment.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class UserAPIService:
    """Handles interactions with AI services using user-provided API keys."""
    
    def __init__(self):
        # No default API key - users must provide their own
        self.default_model = "microsoft/DialoGPT-large"
        logger.info("UserAPIService initialized - users must provide their own API keys")
    
    def generate_response_with_key(self, api_key: str, system_instruction: str, message: str, 
                                 model: str = None) -> str:
        """
        Generate a response using Hugging Face models with a user-provided API key.
        
        Args:
            api_key: User-provided Hugging Face API key
            system_instruction: System prompt or instruction
            message: User message
            model: Specific model to use (optional)
            
        Returns:
            Generated response text
        """
        if not api_key:
            return "API key is required. Please provide your Hugging Face API key."
        
        model = model or self.default_model
        
        # Format the input for conversational models
        # For DialoGPT and similar models, we just need the conversation history
        inputs = f"{system_instruction}\nUser: {message}\nAI:"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
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
                f"https://api-inference.huggingface.co/models/{model}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                else:
                    return str(result)
            elif response.status_code == 401:
                return "Invalid API key. Please check your Hugging Face API key."
            elif response.status_code == 429:
                return "Rate limit exceeded. Please try again later or use a different API key."
            elif response.status_code == 503:
                return "Model is currently loading. Please try again in a few moments."
            else:
                error_msg = f"Error {response.status_code}: {response.text}"
                logger.error(error_msg)
                return f"Error generating response: {error_msg}"
                
        except requests.exceptions.Timeout:
            logger.error("Timeout during Hugging Face API call")
            return "Request timeout. Please try again."
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during Hugging Face API call: {e}")
            return f"Network error: {str(e)}"
        except Exception as e:
            logger.error(f"Error during Hugging Face API call: {e}")
            return f"Error generating response: {str(e)}"
    
    def list_available_models(self) -> List[Dict[str, str]]:
        """
        List some popular free models available on Hugging Face with descriptions.
        """
        return [
            {
                "id": "microsoft/DialoGPT-large",
                "name": "DialoGPT Large",
                "description": "Conversational AI model, good for chat"
            },
            {
                "id": "microsoft/DialoGPT-medium",
                "name": "DialoGPT Medium",
                "description": "Lighter conversational AI model"
            },
            {
                "id": "facebook/blenderbot-400M-distill",
                "name": "Blenderbot 400M",
                "description": "Facebook's conversational model"
            },
            {
                "id": "google/flan-t5-base",
                "name": "FLAN-T5 Base",
                "description": "Instruction-following model"
            },
            {
                "id": "google/flan-t5-small",
                "name": "FLAN-T5 Small",
                "description": "Lighter instruction-following model"
            },
            {
                "id": "gpt2",
                "name": "GPT-2",
                "description": "General text generation model"
            }
        ]
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate a Hugging Face API key by making a simple request.
        
        Args:
            api_key: Hugging Face API key to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not api_key:
            return False
            
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # Make a simple request to validate the key
            response = requests.get(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large",
                headers=headers,
                timeout=10
            )
            
            # Valid key should return 200 or 400 (bad request) but not 401 (unauthorized)
            return response.status_code != 401
        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            return False

# For backwards compatibility
UserService = UserAPIService