"""
Vector Store Module - ChromaDB Management

This module handles all ChromaDB operations for our RAG system.
It's the foundation that stores and retrieves knowledge for our agents.

Key Concepts:
- Collection: Like a database table for a specific type of knowledge
- Embedding: Vector representation of text (handled automatically by ChromaDB)
- Metadata: Additional info we store with each piece of knowledge
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Manages ChromaDB vector database for RAG.
    
    ChromaDB does the heavy lifting:
    1. Converts text to embeddings automatically
    2. Stores embeddings efficiently
    3. Finds similar content via vector search
    
    We just need to:
    - Add knowledge (text + metadata)
    - Query for similar knowledge
    """
    
    def __init__(self, persist_directory: str = "./rag_storage"):
        """
        Initialize ChromaDB client.
        
        Args:
            persist_directory: Where to save the database on disk
        """
        self.persist_dir = Path(persist_directory)
        self.persist_dir.mkdir(exist_ok=True)
        
        # Initialize ChromaDB client
        # persist_directory means data survives across runs
        self.client = chromadb.PersistentClient(
            path=str(self.persist_dir)
        )
        
        logger.info(f"Initialized vector store at {self.persist_dir}")
    
    def get_or_create_collection(
        self, 
        name: str,
        metadata: Optional[Dict] = None
    ) -> chromadb.Collection:
        """
        Get existing collection or create new one.
        
        Collections are like separate tables for different types of knowledge:
        - test_fixes: Error patterns and solutions
        - test_patterns: Reusable code patterns
        - test_plans: Historical test planning decisions
        
        Args:
            name: Collection name
            metadata: Optional metadata for the collection
            
        Returns:
            ChromaDB collection object
        """
        try:
            # ChromaDB requires non-empty metadata, so provide a default
            collection_metadata = metadata if metadata else {"description": name}
            
            collection = self.client.get_or_create_collection(
                name=name,
                metadata=collection_metadata
            )
            logger.info(f"Got/created collection: {name}")
            return collection
        except Exception as e:
            logger.error(f"Error getting collection {name}: {e}")
            raise
    
    def add_knowledge(
        self,
        collection_name: str,
        documents: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ) -> None:
        """
        Add knowledge to a collection.
        
        This is how agents "learn" from past experiences.
        Each piece of knowledge has:
        - document: The actual text (e.g., "Use exact: true for strict locators")
        - metadata: Context (e.g., {"error_type": "locator", "success_rate": 0.95})
        - id: Unique identifier (e.g., "fix_locator_001")
        
        Args:
            collection_name: Which collection to add to
            documents: List of text chunks
            metadatas: List of metadata dicts (same length as documents)
            ids: List of unique IDs (same length as documents)
        """
        collection = self.get_or_create_collection(collection_name)
        
        try:
            # ChromaDB automatically creates embeddings from documents
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(documents)} items to {collection_name}")
        except Exception as e:
            logger.error(f"Error adding to {collection_name}: {e}")
            raise
    
    def search(
        self,
        collection_name: str,
        query: str,
        n_results: int = 3,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Search for similar knowledge.
        
        This is the magic of RAG - finding relevant past knowledge
        based on semantic similarity (meaning, not just keywords).
        
        Example:
        - Query: "locator not found error"
        - Returns: Similar fixes even if exact words differ
        
        Args:
            collection_name: Which collection to search
            query: What to search for
            n_results: How many results to return
            filter_metadata: Optional metadata filters (e.g., {"error_type": "locator"})
            
        Returns:
            Dict with documents, metadatas, distances, ids
        """
        collection = self.get_or_create_collection(collection_name)
        
        try:
            # ChromaDB automatically embeds the query and finds similar documents
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=filter_metadata  # Optional filtering
            )
            
            logger.info(f"Found {len(results['documents'][0])} results for query in {collection_name}")
            return results
        except Exception as e:
            logger.error(f"Error searching {collection_name}: {e}")
            raise
    
    def update_knowledge(
        self,
        collection_name: str,
        ids: List[str],
        documents: Optional[List[str]] = None,
        metadatas: Optional[List[Dict]] = None
    ) -> None:
        """
        Update existing knowledge.
        
        Used when agents improve on existing patterns or
        update success rates based on new data.
        
        Args:
            collection_name: Which collection to update
            ids: IDs of items to update
            documents: New documents (optional)
            metadatas: New metadata (optional)
        """
        collection = self.get_or_create_collection(collection_name)
        
        try:
            collection.update(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            logger.info(f"Updated {len(ids)} items in {collection_name}")
        except Exception as e:
            logger.error(f"Error updating {collection_name}: {e}")
            raise
    
    def delete_knowledge(
        self,
        collection_name: str,
        ids: List[str]
    ) -> None:
        """
        Delete knowledge from collection.
        
        Used to remove outdated or incorrect patterns.
        
        Args:
            collection_name: Which collection
            ids: IDs to delete
        """
        collection = self.get_or_create_collection(collection_name)
        
        try:
            collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} items from {collection_name}")
        except Exception as e:
            logger.error(f"Error deleting from {collection_name}: {e}")
            raise
    
    def get_collection_stats(self, collection_name: str) -> Dict:
        """
        Get statistics about a collection.
        
        Useful for monitoring how much knowledge we've accumulated.
        
        Args:
            collection_name: Which collection
            
        Returns:
            Dict with count and other stats
        """
        collection = self.get_or_create_collection(collection_name)
        
        try:
            count = collection.count()
            return {
                "name": collection_name,
                "count": count,
                "metadata": collection.metadata
            }
        except Exception as e:
            logger.error(f"Error getting stats for {collection_name}: {e}")
            raise
    
    def list_collections(self) -> List[str]:
        """
        List all collections in the database.
        
        Returns:
            List of collection names
        """
        try:
            collections = self.client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            logger.error(f"Error listing collections: {e}")
            raise
