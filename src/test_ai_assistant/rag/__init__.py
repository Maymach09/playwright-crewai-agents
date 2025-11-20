"""
RAG (Retrieval-Augmented Generation) Module

This module provides RAG capabilities for the test AI assistant.
It uses ChromaDB for vector storage and retrieval.

Main Components:
- VectorStore: Low-level ChromaDB operations
- KnowledgeBase: Initial knowledge to seed the system
- RAGRetriever: High-level interface for agents

Usage:
    from src.test_ai_assistant.rag import RAGRetriever
    
    retriever = RAGRetriever()
    retriever.initialize_knowledge_base()
    
    # Search for fixes
    fixes = retriever.search_fixes("locator not found")
    
    # Search for patterns
    patterns = retriever.search_patterns("fill a form")
"""

from .vector_store import VectorStore
from .knowledge_base import InitialKnowledge, KnowledgeItem
from .retriever import RAGRetriever

__all__ = [
    'VectorStore',
    'InitialKnowledge',
    'KnowledgeItem',
    'RAGRetriever'
]
