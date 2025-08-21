"""
Bot service for the child bot system.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

from src.models.bot import Bot
from src.models.conversation import Conversation
from src.services.llm_service import LLMService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BotService:
    """
    Service for managing and interacting with bots.
    """
    
    def __init__(self, data_dir: str = None, llm_service: LLMService = None):
        """
        Initialize the bot service.
        
        Args:
            data_dir: Directory for storing bot data
            llm_service: LLM service for generating responses
        """
        self.data_dir = data_dir or os.environ.get("BOT_DATA_DIR", "data")
        self.bots_dir = os.path.join(self.data_dir, "bots")
        self.conversations_dir = os.path.join(self.data_dir, "conversations")
        self.llm_service = llm_service or LLMService()
        
        # Create directories if they don't exist
        os.makedirs(self.bots_dir, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)
    
    def create_bot(self, bot_data: Dict[str, Any]) -> Bot:
        """
        Create a new bot.
        
        Args:
            bot_data: Data for the new bot
            
        Returns:
            The created bot
        """
        bot = Bot(
            name=bot_data.get("name", "Unnamed Bot"),
            description=bot_data.get("description", ""),
            system_prompt=bot_data.get("system_prompt", "You are a helpful assistant."),
            focus_keywords=bot_data.get("focus_keywords", []),
            icon=bot_data.get("icon"),
            parent_id=bot_data.get("parent_id"),
            model_config=bot_data.get("model_config")
        )
        
        bot.save(self.bots_dir)
        logger.info(f"Created bot: {bot.id} - {bot.name}")
        
        return bot
    
    def get_bot(self, bot_id: str) -> Optional[Bot]:
        """
        Get a bot by ID.
        
        Args:
            bot_id: ID of the bot to get
            
        Returns:
            The bot or None if not found
        """
        file_path = os.path.join(self.bots_dir, f"{bot_id}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Bot not found: {bot_id}")
            return None
        
        try:
            return Bot.load(file_path)
        except Exception as e:
            logger.exception(f"Error loading bot: {bot_id}")
            return None
    
    def update_bot(self, bot_id: str, bot_data: Dict[str, Any]) -> Optional[Bot]:
        """
        Update a bot.
        
        Args:
            bot_id: ID of the bot to update
            bot_data: New data for the bot
            
        Returns:
            The updated bot or None if not found
        """
        bot = self.get_bot(bot_id)
        
        if not bot:
            return None
        
        # Update bot fields
        if "name" in bot_data:
            bot.name = bot_data["name"]
        if "description" in bot_data:
            bot.description = bot_data["description"]
        if "system_prompt" in bot_data:
            bot.system_prompt = bot_data["system_prompt"]
        if "focus_keywords" in bot_data:
            bot.focus_keywords = bot_data["focus_keywords"]
        if "icon" in bot_data:
            bot.icon = bot_data["icon"]
        if "model_config" in bot_data:
            bot.model_config = bot_data["model_config"]
        
        bot.save(self.bots_dir)
        logger.info(f"Updated bot: {bot.id} - {bot.name}")
        
        return bot
    
    def delete_bot(self, bot_id: str) -> bool:
        """
        Delete a bot.
        
        Args:
            bot_id: ID of the bot to delete
            
        Returns:
            True if the bot was deleted, False otherwise
        """
        file_path = os.path.join(self.bots_dir, f"{bot_id}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Bot not found for deletion: {bot_id}")
            return False
        
        try:
            os.remove(file_path)
            logger.info(f"Deleted bot: {bot_id}")
            return True
        except Exception as e:
            logger.exception(f"Error deleting bot: {bot_id}")
            return False
    
    def list_bots(self) -> List[Bot]:
        """
        List all bots.
        
        Returns:
            List of bots
        """
        return Bot.list_bots(self.bots_dir)
    
    def create_conversation(self, bot_id: str, user_id: str = "anonymous") -> Optional[Conversation]:
        """
        Create a new conversation with a bot.
        
        Args:
            bot_id: ID of the bot to converse with
            user_id: ID of the user
            
        Returns:
            The created conversation or None if the bot doesn't exist
        """
        bot = self.get_bot(bot_id)
        
        if not bot:
            return None
        
        conversation = Conversation(
            bot_id=bot_id,
            user_id=user_id,
            metadata={"system_prompt": bot.system_prompt}
        )
        
        conversation_dir = os.path.join(self.conversations_dir, bot_id)
        os.makedirs(conversation_dir, exist_ok=True)
        
        conversation.save(conversation_dir)
        logger.info(f"Created conversation: {conversation.id} for bot: {bot_id}")
        
        return conversation
    
    def get_conversation(self, conversation_id: str, bot_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            conversation_id: ID of the conversation to get
            bot_id: ID of the bot
            
        Returns:
            The conversation or None if not found
        """
        conversation_dir = os.path.join(self.conversations_dir, bot_id)
        file_path = os.path.join(conversation_dir, f"{conversation_id}.json")
        
        if not os.path.exists(file_path):
            logger.warning(f"Conversation not found: {conversation_id}")
            return None
        
        try:
            return Conversation.load(file_path)
        except Exception as e:
            logger.exception(f"Error loading conversation: {conversation_id}")
            return None
    
    def list_conversations(self, bot_id: str, user_id: str = None) -> List[Conversation]:
        """
        List conversations for a bot.
        
        Args:
            bot_id: ID of the bot
            user_id: Optional user ID to filter by
            
        Returns:
            List of conversations
        """
        conversation_dir = os.path.join(self.conversations_dir, bot_id)
        return Conversation.list_conversations(conversation_dir, bot_id, user_id)
    
    def send_message(
        self,
        conversation_id: str,
        bot_id: str,
        message: str,
        user_id: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Send a message to a bot and get a response.
        
        Args:
            conversation_id: ID of the conversation
            bot_id: ID of the bot
            message: Message to send
            user_id: ID of the user
            
        Returns:
            Response from the bot
        """
        # Get the conversation or create a new one if it doesn't exist
        conversation = self.get_conversation(conversation_id, bot_id)
        if not conversation:
            conversation = self.create_conversation(bot_id, user_id)
            if not conversation:
                return {"error": f"Bot not found: {bot_id}"}
        
        # Get the bot
        bot = self.get_bot(bot_id)
        if not bot:
            return {"error": f"Bot not found: {bot_id}"}
        
        # Add the user message to the conversation
        conversation.add_message("user", message)
        
        # Get the conversation context for the LLM
        context = conversation.get_context_for_llm()
        
        # Get the bot's response from the LLM
        llm_response = self.llm_service.chat_completion(
            messages=context,
            model=bot.model_config.get("model", "vicuna-13b"),
            temperature=bot.model_config.get("temperature", 0.7),
            max_tokens=bot.model_config.get("max_tokens", 1024)
        )
        
        # Extract the assistant's message
        assistant_message = self.llm_service.extract_assistant_message(llm_response)
        
        if assistant_message:
            # Add the assistant's message to the conversation
            conversation.add_message("assistant", assistant_message)
            
            # Save the conversation
            conversation_dir = os.path.join(self.conversations_dir, bot_id)
            conversation.save(conversation_dir)
            
            return {
                "conversation_id": conversation.id,
                "bot_id": bot.id,
                "message": assistant_message
            }
        else:
            return {
                "conversation_id": conversation.id,
                "bot_id": bot.id,
                "error": "Failed to get response from LLM",
                "details": llm_response
            }

