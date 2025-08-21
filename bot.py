"""
Bot model for the chatbot system.
Adapted from the production-grade project with simplified implementation.
"""

import os
import json
import time
import uuid
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class Bot:
    """
    Represents a chatbot with specific persona and configuration.
    """
    
    def __init__(
        self,
        name: str,
        description: str = "",
        system_prompt: str = "You are a helpful assistant.",
        focus_keywords: List[str] = None,
        icon: str = None,
        parent_id: str = None,
        model_config: Dict[str, Any] = None,
        id: str = None,
        created_at: float = None,
        updated_at: float = None
    ):
        """
        Initialize a new Bot instance.
        
        Args:
            name: The name of the bot
            description: A description of the bot
            system_prompt: System prompt for the bot
            focus_keywords: Keywords that the bot focuses on
            icon: Icon for the bot
            parent_id: ID of the parent bot (if this is a child bot)
            model_config: Configuration for the model
            id: Unique identifier for the bot (generated if not provided)
            created_at: Timestamp when the bot was created
            updated_at: Timestamp when the bot was last updated
        """
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.focus_keywords = focus_keywords or []
        self.icon = icon
        self.parent_id = parent_id
        self.model_config = model_config or {"model": "gemini-1.5-flash", "temperature": 0.7, "max_tokens": 1024}
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or time.time()
        self.updated_at = updated_at or time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the bot to a dictionary.
        
        Returns:
            Dict representation of the bot
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "focus_keywords": self.focus_keywords,
            "icon": self.icon,
            "parent_id": self.parent_id,
            "model_config": self.model_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Bot':
        """
        Create a Bot instance from a dictionary.
        
        Args:
            data: Dictionary containing bot data
            
        Returns:
            Bot instance
        """
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            system_prompt=data.get("system_prompt"),
            focus_keywords=data.get("focus_keywords"),
            icon=data.get("icon"),
            parent_id=data.get("parent_id"),
            model_config=data.get("model_config"),
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def save(self, directory: str) -> str:
        """
        Save the bot to a JSON file.
        
        Args:
            directory: Directory to save the bot in
            
        Returns:
            Path to the saved file
        """
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{self.id}.json")
        
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return file_path
    
    @classmethod
    def load(cls, file_path: str) -> 'Bot':
        """
        Load a bot from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Bot instance
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def list_bots(cls, directory: str) -> List['Bot']:
        """
        List all bots in a directory.
        
        Args:
            directory: Directory containing bot JSON files
            
        Returns:
            List of Bot instances
        """
        bots = []
        
        if not os.path.exists(directory):
            return bots
        
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                try:
                    bot = cls.load(file_path)
                    bots.append(bot)
                except Exception as e:
                    logger.error(f"Error loading bot from {file_path}: {e}")
        
        return bots
