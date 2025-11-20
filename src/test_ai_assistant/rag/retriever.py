"""
Retriever Module - RAG Query Interface

This module provides a simple interface for agents to query
the RAG system. It handles the complexity of searching and
formatting results.

Agents call this module instead of directly using VectorStore.
"""

from typing import List, Dict, Optional
import logging
from .vector_store import VectorStore
from .knowledge_base import InitialKnowledge

logger = logging.getLogger(__name__)


class RAGRetriever:
    """
    High-level interface for RAG queries.
    
    This is what agents use to get relevant knowledge.
    It abstracts away the complexity of vector search.
    """
    
    def __init__(self, persist_directory: str = "./rag_storage"):
        """
        Initialize retriever with vector store.
        
        Args:
            persist_directory: Where ChromaDB stores data
        """
        self.vector_store = VectorStore(persist_directory)
        self.initialized = False
        logger.info("RAG Retriever initialized")
    
    def initialize_knowledge_base(self) -> None:
        """
        Seed the vector store with initial knowledge.
        
        This should be called once when setting up RAG.
        It populates the database with our initial patterns.
        """
        if self.initialized:
            logger.info("Knowledge base already initialized")
            return
        
        logger.info("Initializing knowledge base...")
        
        # Get all initial knowledge
        all_knowledge = InitialKnowledge.get_all_knowledge()
        
        # Populate each collection
        for collection_name, items in all_knowledge.items():
            documents = [item.content for item in items]
            metadatas = [item.metadata for item in items]
            ids = [item.id for item in items]
            
            try:
                self.vector_store.add_knowledge(
                    collection_name=collection_name,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Initialized {collection_name} with {len(items)} items")
            except Exception as e:
                logger.error(f"Error initializing {collection_name}: {e}")
                # Continue with other collections even if one fails
        
        self.initialized = True
        logger.info("Knowledge base initialization complete")
    
    def search_fixes(
        self,
        error_message: str,
        n_results: int = 3,
        error_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant fix patterns based on error.
        
        This is used by the Healer agent to find solutions.
        
        Args:
            error_message: The error to fix
            n_results: How many fixes to return
            error_type: Optional filter (e.g., "locator", "timeout")
            
        Returns:
            List of fix patterns with content and metadata
            
        Example:
            fixes = retriever.search_fixes(
                error_message="locator not found",
                error_type="locator"
            )
            # Returns relevant locator fix patterns
        """
        try:
            # Build metadata filter if error_type provided
            filter_metadata = {"error_type": error_type} if error_type else None
            
            # Search the test_fixes collection
            results = self.vector_store.search(
                collection_name="test_fixes",
                query=error_message,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            # Format results for easy consumption
            fixes = []
            for i, doc in enumerate(results['documents'][0]):
                fixes.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "similarity": 1 - results['distances'][0][i]  # Convert distance to similarity
                })
            
            logger.info(f"Found {len(fixes)} fixes for: {error_message[:50]}...")
            return fixes
            
        except Exception as e:
            logger.error(f"Error searching fixes: {e}")
            return []
    
    def search_patterns(
        self,
        task_description: str,
        n_results: int = 3,
        pattern_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant code patterns.
        
        This is used by the Generator agent to find
        reusable code templates.
        
        Args:
            task_description: What the test needs to do
            n_results: How many patterns to return
            pattern_type: Optional filter (e.g., "navigation", "form")
            
        Returns:
            List of code patterns with content and metadata
            
        Example:
            patterns = retriever.search_patterns(
                task_description="fill a form and submit",
                pattern_type="form"
            )
            # Returns form interaction patterns
        """
        try:
            filter_metadata = {"pattern_type": pattern_type} if pattern_type else None
            
            results = self.vector_store.search(
                collection_name="code_patterns",
                query=task_description,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            patterns = []
            for i, doc in enumerate(results['documents'][0]):
                patterns.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "similarity": 1 - results['distances'][0][i]
                })
            
            logger.info(f"Found {len(patterns)} patterns for: {task_description[:50]}...")
            return patterns
            
        except Exception as e:
            logger.error(f"Error searching patterns: {e}")
            return []
    
    def search_test_plans(
        self,
        scenario_description: str,
        n_results: int = 2,
        plan_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for relevant test plan templates.
        
        This is used by the Planner agent to structure tests.
        
        Args:
            scenario_description: What needs to be tested
            n_results: How many templates to return
            plan_type: Optional filter (e.g., "smoke", "e2e", "crud")
            
        Returns:
            List of test plan templates
            
        Example:
            plans = retriever.search_test_plans(
                scenario_description="test user login and dashboard",
                plan_type="e2e"
            )
            # Returns end-to-end test structure templates
        """
        try:
            filter_metadata = {"plan_type": plan_type} if plan_type else None
            
            results = self.vector_store.search(
                collection_name="test_plans",
                query=scenario_description,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            plans = []
            for i, doc in enumerate(results['documents'][0]):
                plans.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "similarity": 1 - results['distances'][0][i]
                })
            
            logger.info(f"Found {len(plans)} test plans for: {scenario_description[:50]}...")
            return plans
            
        except Exception as e:
            logger.error(f"Error searching test plans: {e}")
            return []
    
    def add_successful_fix(
        self,
        error_message: str,
        fix_applied: str,
        error_type: str,
        test_file: str
    ) -> None:
        """
        Add a successful fix to the knowledge base.
        
        This is the FEEDBACK LOOP - when the Healer successfully
        fixes a test, we store that solution for future use.
        
        Args:
            error_message: The error that was fixed
            fix_applied: The solution that worked
            error_type: Category of error
            test_file: Which test was fixed
            
        Example:
            retriever.add_successful_fix(
                error_message="locator 'button' not found",
                fix_applied="Added waitForSelector with 10s timeout",
                error_type="locator",
                test_file="login.spec.ts"
            )
        """
        try:
            # Generate unique ID based on timestamp and test file
            import time
            fix_id = f"fix_learned_{int(time.time())}_{hash(test_file) % 10000}"
            
            # Create metadata
            metadata = {
                "error_type": error_type,
                "error_pattern": error_message[:100],  # Store snippet
                "success_rate": 1.0,  # Initial success rate
                "tags": f"learned,{error_type}",
                "source": test_file,
                "learned_at": time.time()
            }
            
            # Add to test_fixes collection
            self.vector_store.add_knowledge(
                collection_name="test_fixes",
                documents=[fix_applied],
                metadatas=[metadata],
                ids=[fix_id]
            )
            
            logger.info(f"Added learned fix: {fix_id}")
            
        except Exception as e:
            logger.error(f"Error adding successful fix: {e}")
    
    def add_code_pattern(
        self,
        pattern_code: str,
        pattern_type: str,
        description: str,
        tags: List[str]
    ) -> None:
        """
        Add a new code pattern to the knowledge base.
        
        When the Generator creates particularly good code,
        we can store it as a reusable pattern.
        
        Args:
            pattern_code: The code snippet
            pattern_type: Category (e.g., "navigation", "form")
            description: What this pattern does
            tags: Searchable tags (list will be converted to comma-separated string)
        """
        try:
            import time
            pattern_id = f"pattern_learned_{int(time.time())}_{hash(pattern_code) % 10000}"
            
            # Convert tags list to comma-separated string
            tags_str = ",".join(tags + ["learned"])
            
            metadata = {
                "pattern_type": pattern_type,
                "description": description,
                "complexity": "simple",  # Could be determined by code length
                "tags": tags_str,
                "learned_at": time.time()
            }
            
            self.vector_store.add_knowledge(
                collection_name="code_patterns",
                documents=[pattern_code],
                metadatas=[metadata],
                ids=[pattern_id]
            )
            
            logger.info(f"Added learned pattern: {pattern_id}")
            
        except Exception as e:
            logger.error(f"Error adding code pattern: {e}")
    
    def search_application_knowledge(
        self,
        scenario_description: str,
        n_results: int = 3,
        application: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for discovered application structure and flows.
        
        This is used by the Planner to check if we've already
        explored this part of the application.
        
        Args:
            scenario_description: What needs to be tested
            n_results: How many results to return
            application: Optional filter (e.g., "salesforce", "shopify")
            
        Returns:
            List of application knowledge with UI details
            
        Example:
            knowledge = retriever.search_application_knowledge(
                scenario_description="create account salesforce",
                application="salesforce"
            )
            # Returns: Previously discovered Account creation flow with locators
        """
        try:
            filter_metadata = {"application": application} if application else None
            
            results = self.vector_store.search(
                collection_name="application_knowledge",
                query=scenario_description,
                n_results=n_results,
                filter_metadata=filter_metadata
            )
            
            knowledge = []
            for i, doc in enumerate(results['documents'][0]):
                knowledge.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "id": results['ids'][0][i],
                    "similarity": 1 - results['distances'][0][i]
                })
            
            logger.info(f"Found {len(knowledge)} application knowledge items for: {scenario_description[:50]}...")
            return knowledge
            
        except Exception as e:
            logger.error(f"Error searching application knowledge: {e}")
            return []
    
    def add_application_knowledge(
        self,
        scenario: str,
        navigation_path: str,
        elements_discovered: str,
        application: str,
        module: str,
        action: str
    ) -> None:
        """
        Store discovered application structure for reuse.
        
        This is the LEARNING LOOP for the Planner - when it explores
        the application, we cache what it learned for future tests.
        
        Args:
            scenario: High-level description (e.g., "Create Account in Salesforce")
            navigation_path: Steps to reach this feature (e.g., "Home → Accounts → New")
            elements_discovered: Detailed UI elements and locators (formatted text)
            application: App name (e.g., "salesforce", "shopify")
            module: Module/section (e.g., "accounts", "products")
            action: What action (e.g., "create", "edit", "view")
            
        Example:
            retriever.add_application_knowledge(
                scenario="Create new account with required fields",
                navigation_path="Home → Accounts → New button",
                elements_discovered='''Required Fields:
                - Account Name: getByRole('textbox', { name: 'Account Name' })
                Actions:
                - Save: getByRole('button', { name: 'Save' })''',
                application="salesforce",
                module="accounts",
                action="create"
            )
        """
        try:
            import time
            knowledge_id = f"app_{application}_{module}_{action}_{int(time.time())}"
            
            # Combine all info into searchable content
            content = f"""{scenario}
Navigation: {navigation_path}
{elements_discovered}"""
            
            metadata = {
                "application": application,
                "module": module,
                "action": action,
                "last_verified": str(time.time()),
                "tags": f"{application},{module},{action},discovered"
            }
            
            self.vector_store.add_knowledge(
                collection_name="application_knowledge",
                documents=[content],
                metadatas=[metadata],
                ids=[knowledge_id]
            )
            
            logger.info(f"Added application knowledge: {knowledge_id}")
            
        except Exception as e:
            logger.error(f"Error adding application knowledge: {e}")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the knowledge base.
        
        Useful for monitoring RAG growth over time.
        
        Returns:
            Dict with collection names and item counts
        """
        try:
            collections = ["test_fixes", "code_patterns", "test_plans", "application_knowledge"]
            stats = {}
            
            for collection in collections:
                collection_stats = self.vector_store.get_collection_stats(collection)
                stats[collection] = collection_stats
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
