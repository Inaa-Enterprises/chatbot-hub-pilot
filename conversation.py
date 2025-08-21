"""
Conversation model for the chatbot backend.
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

class Message:
    """
    Represents a message in a conversation.
    """
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        """
        Initialize a message.
        
        Args:
            role: The role of the message sender (user or assistant)
            content: The content of the message
            timestamp: The timestamp of the message
        """
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary.
        
        Returns:
            Dictionary representation of the message
        """
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """
        Create a message from a dictionary.
        
        Args:
            data: Dictionary representation of the message
            
        Returns:
            Message object
        """
        timestamp = datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=timestamp
        )


class Conversation:
    """
    Represents a conversation between a user and the chatbot.
    """
    
    def __init__(self, id: Optional[str] = None, user_id: Optional[str] = None):
        """
        Initialize a conversation.
        
        Args:
            id: The ID of the conversation
            user_id: The ID of the user
        """
        self.id = id or str(uuid.uuid4())
        self.user_id = user_id
        self.messages: List[Message] = []
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.questionnaire: Optional[Dict[str, Any]] = None
        self.original_message: Optional[str] = None
    
    def add_message(self, role: str, content: str) -> Message:
        """
        Add a message to the conversation.
        
        Args:
            role: The role of the message sender (user or assistant)
            content: The content of the message
            
        Returns:
            The added message
        """
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message
    
    def start_questionnaire(self, template_id: str, original_message: str) -> None:
        """
        Start a questionnaire for prompt enhancement.
        
        Args:
            template_id: The ID of the questionnaire template
            original_message: The original user message that triggered the questionnaire
        """
        self.questionnaire = {
            "templateId": template_id,
            "currentQuestionIndex": 0,
            "answers": {},
            "complete": False
        }
        self.original_message = original_message
    
    def complete_questionnaire(self) -> None:
        """
        Mark the questionnaire as complete.
        """
        if self.questionnaire:
            self.questionnaire["complete"] = True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the conversation to a dictionary.
        
        Returns:
            Dictionary representation of the conversation
        """
        return {
            "id": self.id,
            "userId": self.user_id,
            "messages": [message.to_dict() for message in self.messages],
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "questionnaire": self.questionnaire,
            "originalMessage": self.original_message
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        """
        Create a conversation from a dictionary.
        
        Args:
            data: Dictionary representation of the conversation
            
        Returns:
            Conversation object
        """
        conversation = cls(
            id=data.get("id"),
            user_id=data.get("userId")
        )
        
        conversation.messages = [Message.from_dict(message_data) for message_data in data.get("messages", [])]
        conversation.created_at = datetime.fromisoformat(data["createdAt"]) if "createdAt" in data else datetime.now()
        conversation.updated_at = datetime.fromisoformat(data["updatedAt"]) if "updatedAt" in data else datetime.now()
        conversation.questionnaire = data.get("questionnaire")
        conversation.original_message = data.get("originalMessage")
        
        return conversation


class ConversationManager:
    """
    Manages conversations for the chatbot.
    """
    
    def __init__(self):
        """
        Initialize the conversation manager.
        """
        self.conversations: Dict[str, Conversation] = {}
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            The conversation or None if not found
        """
        return self.conversations.get(conversation_id)
    
    def get_or_create_conversation(self, user_id: Optional[str] = None, conversation_id: Optional[str] = None) -> Conversation:
        """
        Get a conversation by ID or create a new one.
        
        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            
        Returns:
            The conversation
        """
        if conversation_id and conversation_id in self.conversations:
            return self.conversations[conversation_id]
        
        conversation = Conversation(id=conversation_id, user_id=user_id)
        self.conversations[conversation.id] = conversation
        return conversation
    
    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        """
        Get all conversations for a user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of conversations
        """
        return [conversation for conversation in self.conversations.values() if conversation.user_id == user_id]
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation.
        
        Args:
            conversation_id: The ID of the conversation
            
        Returns:
            True if the conversation was deleted, False otherwise
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False


# Initialize the conversation manager
conversation_manager = ConversationManager()
