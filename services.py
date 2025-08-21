"""
Enhanced AI service with support for multiple LLM providers.
Integrates Gemini, Hugging Face, and Vicuna (placeholder).
"""

import os
import logging
import asyncio
from typing import Dict, List, Any, AsyncGenerator, Optional

# Try to import Google Cloud AI Platform (optional)
try:
    import google.cloud.aiplatform as aiplatform
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    aiplatform = None

logger = logging.getLogger(__name__)

# --- Configuration --- 
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-001")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "huggingface").lower()  # Default to huggingface
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
VICUNA_API_URL = os.getenv("VICUNA_API_URL", "http://localhost:8000/v1")

class AIService:
    """Handles interactions with the configured AI model provider."""
    
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.gemini_model = None
        
        if self.provider == "gemini":
            if not GOOGLE_AI_AVAILABLE:
                raise RuntimeError("Google Cloud AI Platform not available. Install with: pip install google-cloud-aiplatform")
            
            if not GCP_PROJECT_ID:
                raise ValueError("GCP_PROJECT_ID must be set when using Gemini provider")
            try:
                aiplatform.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)
                # NOTE: Using Vertex AI SDK for Gemini models
                self.gemini_model = aiplatform.gapic.PredictionServiceClient()
                # Construct the full model endpoint path for Vertex AI
                self.model_endpoint = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION}/publishers/google/models/{GEMINI_MODEL_NAME}"
                logger.info(f"AIService initialized for Gemini provider using model endpoint: {self.model_endpoint}")
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud AI Platform for Gemini: {e}")
                raise RuntimeError(f"Gemini initialization failed: {e}")
        elif self.provider == "huggingface":
            if not HUGGING_FACE_API_KEY:
                logger.warning("HUGGING_FACE_API_KEY not set. Hugging Face service will not work.")
            logger.info("AIService initialized for Hugging Face provider.")
        elif self.provider == "vicuna":
            # Placeholder: No specific initialization needed for the Vicuna placeholder yet.
            logger.info("AIService initialized for Vicuna provider (placeholder). Ensure local model server is running if applicable.")
        else:
            raise ValueError(f"Unsupported LLM_PROVIDER: {self.provider}. Choose 'gemini', 'huggingface' or 'vicuna'.")

    async def _generate_gemini_streaming_response(self, system_instruction: str, message: str):
        """Generates streaming response using Gemini via Vertex AI SDK."""
        if not self.gemini_model:
             raise RuntimeError("Gemini model not initialized.")
        
        try:
            # Construct the request payload for Vertex AI streaming prediction
            # This is a simplified example; refer to Vertex AI documentation for exact payload structure.
            instance = {
                "prompt": f"{system_instruction}\n\nUser: {message}\nAI:"
            }
            parameters = {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            }
            
            # --- Placeholder Response --- 
            # Since implementing the actual Vertex AI streaming call is complex,
            # we will yield a placeholder response for now.
            logger.warning("Using placeholder response for Gemini streaming - Vertex AI stream_predict needs implementation.")
            yield "I'm responding based on your message: " + message[:30] + "..."
            yield " This is a placeholder response from the Gemini model."
            yield " In production, this would be a real response from the Vertex AI API."
            
        except Exception as e:
            logger.error(f"Error during Gemini streaming generation: {e}")
            raise RuntimeError(f"Gemini API call failed: {e}")

    async def _generate_huggingface_response(self, system_instruction: str, message: str):
        """Generates response using Hugging Face models."""
        try:
            from huggingface_service import HuggingFaceService
            hf_service = HuggingFaceService()
            
            response = hf_service.generate_response(system_instruction, message)
            yield response
            
        except Exception as e:
            logger.error(f"Error during Hugging Face generation: {e}")
            yield f"Error generating response: {str(e)}"

    async def _generate_vicuna_streaming_response(self, system_instruction: str, message: str):
        """Placeholder for generating streaming response using Vicuna."""
        logger.info("Generating response using Vicuna provider (placeholder)...")
        # In a real implementation, this would interact with a local Vicuna server/API.
        yield f"[Vicuna Model] Response to: \"{message[:30]}...\"\n"
        yield "This is a placeholder response from the Vicuna model integration."
        yield f"\nSystem instruction used: \"{system_instruction[:50]}...\""
        # Simulate streaming delay
        await asyncio.sleep(0.5)

    async def generate_streaming_response(self, system_instruction: str, message: str):
        """Generates a streaming response based on the configured provider."""
        if self.provider == "gemini":
            async for chunk in self._generate_gemini_streaming_response(system_instruction, message):
                yield chunk
        elif self.provider == "huggingface":
            async for chunk in self._generate_huggingface_response(system_instruction, message):
                yield chunk
        elif self.provider == "vicuna":
            async for chunk in self._generate_vicuna_streaming_response(system_instruction, message):
                yield chunk
        else:
            # This case should ideally be caught in __init__, but as a safeguard:
            logger.error(f"Attempted to generate response with unsupported provider: {self.provider}")
            raise RuntimeError(f"Unsupported LLM provider configured: {self.provider}")