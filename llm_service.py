"""
LLM service for the child bot system.
"""

import os
import requests
import json
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for interacting with language models.
    """
    
    def __init__(self, api_url: str = None, api_key: str = None):
        """
        Initialize the LLM service.
        
        Args:
            api_url: URL of the LLM API server
            api_key: API key for authentication
        """
        self.api_url = api_url or os.environ.get("LLM_API_URL", "http://localhost:3001/api")
        self.api_key = api_key or os.environ.get("LLM_API_KEY", "test-api-key")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "vicuna-13b",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        force_cloud: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a chat completion.
        
        Args:
            messages: List of messages in the conversation
            model: Model to use for generation
            temperature: Temperature for generation
            max_tokens: Maximum number of tokens to generate
            force_cloud: Whether to force using the cloud model
            
        Returns:
            Response from the LLM API
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key
            }
            
            data = {
                "messages": messages,
                "options": {
                    "model": model,
                    "temperature": temperature,
                    "maxTokens": max_tokens,
                    "forceCloud": force_cloud
                }
            }
            
            response = requests.post(
                f"{self.api_url}/chat",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error from LLM API: {response.status_code} - {response.text}")
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text
                }
        
        except Exception as e:
            logger.exception("Error calling LLM API")
            return {
                "error": "Service error",
                "details": str(e)
            }
    
    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available models.
        
        Returns:
            List of available models
        """
        try:
            headers = {
                "X-API-Key": self.api_key
            }
            
            response = requests.get(
                f"{self.api_url}/models",
                headers=headers
            )
            
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                logger.error(f"Error getting models: {response.status_code} - {response.text}")
                return []
        
        except Exception as e:
            logger.exception("Error getting models")
            return []
    
    def extract_assistant_message(self, response: Dict[str, Any]) -> Optional[str]:
        """
        Extract the assistant's message from an LLM API response.
        
        Args:
            response: Response from the LLM API
            
        Returns:
            Assistant's message or None if not found
        """
        try:
            if "error" in response:
                return f"Error: {response['error']}"
            
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            
            return None
        
        except Exception as e:
            logger.exception("Error extracting assistant message")
            return None

