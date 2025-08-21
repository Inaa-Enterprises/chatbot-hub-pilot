"""
Knowledge base model for the child bot system.
"""

import os
import json
import time
import uuid
from typing import Dict, List, Optional, Any

class KnowledgeBase:
    """
    Represents a knowledge base for a child bot.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        id: str = None,
        created_at: float = None,
        updated_at: float = None,
        sources: List[Dict[str, Any]] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        vector_db_path: str = None
    ):
        """
        Initialize a new KnowledgeBase instance.
        
        Args:
            name: The name of the knowledge base
            description: A description of the knowledge base
            id: Unique identifier for the knowledge base (generated if not provided)
            created_at: Timestamp when the knowledge base was created
            updated_at: Timestamp when the knowledge base was last updated
            sources: List of sources (files, URLs, etc.) in the knowledge base
            embedding_model: Name of the embedding model to use
            vector_db_path: Path to the vector database file
        """
        self.name = name
        self.description = description
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or time.time()
        self.updated_at = updated_at or time.time()
        self.sources = sources or []
        self.embedding_model = embedding_model
        self.vector_db_path = vector_db_path or f"knowledge_bases/{self.id}/vector_db"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the knowledge base to a dictionary.
        
        Returns:
            Dict representation of the knowledge base
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "sources": self.sources,
            "embedding_model": self.embedding_model,
            "vector_db_path": self.vector_db_path
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgeBase':
        """
        Create a KnowledgeBase instance from a dictionary.
        
        Args:
            data: Dictionary containing knowledge base data
            
        Returns:
            KnowledgeBase instance
        """
        return cls(
            name=data.get("name"),
            description=data.get("description"),
            id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            sources=data.get("sources"),
            embedding_model=data.get("embedding_model"),
            vector_db_path=data.get("vector_db_path")
        )
    
    def save(self, directory: str) -> str:
        """
        Save the knowledge base to a JSON file.
        
        Args:
            directory: Directory to save the knowledge base in
            
        Returns:
            Path to the saved file
        """
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{self.id}.json")
        
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        
        return file_path
    
    @classmethod
    def load(cls, file_path: str) -> 'KnowledgeBase':
        """
        Load a knowledge base from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            KnowledgeBase instance
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def list_knowledge_bases(cls, directory: str) -> List['KnowledgeBase']:
        """
        List all knowledge bases in a directory.
        
        Args:
            directory: Directory containing knowledge base JSON files
            
        Returns:
            List of KnowledgeBase instances
        """
        knowledge_bases = []
        
        if not os.path.exists(directory):
            return knowledge_bases
        
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                file_path = os.path.join(directory, filename)
                try:
                    kb = cls.load(file_path)
                    knowledge_bases.append(kb)
                except Exception as e:
                    print(f"Error loading knowledge base from {file_path}: {e}")
        
        return knowledge_bases
    
    def add_source(self, source_type: str, source_path: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Add a source to the knowledge base.
        
        Args:
            source_type: Type of source (file, url, text)
            source_path: Path or URL to the source
            metadata: Additional metadata about the source
            
        Returns:
            The added source
        """
        source = {
            "id": str(uuid.uuid4()),
            "type": source_type,
            "path": source_path,
            "added_at": time.time(),
            "metadata": metadata or {}
        }
        
        self.sources.append(source)
        self.updated_at = time.time()
        
        return source
    
    def remove_source(self, source_id: str) -> bool:
        """
        Remove a source from the knowledge base.
        
        Args:
            source_id: ID of the source to remove
            
        Returns:
            True if the source was removed, False otherwise
        """
        for i, source in enumerate(self.sources):
            if source.get("id") == source_id:
                self.sources.pop(i)
                self.updated_at = time.time()
                return True
        
        return False

