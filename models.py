# Pydantic models for API requests and responses

from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    personaId: str # Matches the ID used in the frontend (e.g., 'synapse', 'tutor')
    # Add other fields if needed based on frontend, e.g., history
    # history: Optional[list[dict]] = None

# No specific response model needed for streaming text, but we might add one later if needed.

