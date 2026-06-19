import os
from typing import List, Dict
from pathlib import Path
from retriever import DocumentRetriever
from embedder import DocumentEmbedder
from vector_db import VectorDatabase
from llm_interface import OllamaInterface
import numpy as np


class RAGPipeline:
    """Complete Retrieval Augmented Generation Pipeline with Ollama"""
    
    def __init__(self, use_cached_embeddings: bool = True, model: str = "mistral"):
        """Initialize the RAG pipeline"""
        print("=" * 70)
        print("Initializing RAG Pipeline with Ollama")
        print("=" * 70 + "\n")
        
        # Initialize components
        print("1. Initializing document retriever...")
        self.retriever = DocumentRetriever()
        
        print("2. Initializing embedder...")
        self.embedder = DocumentEmbedder()
        
        print("3. Initializing vector database...")
        self.vector_db = VectorDatabase()
        
        print("4. Initializing Ollama LLM interface...")
        try:
            self.llm = OllamaInterface(model=model)
        except Exception as e:
            print(f"\nError: {e}")
            print("\nMake sure Ollama is running:")
            print("  In a new terminal, run: ollama serve")
            raise
        
        print("5. Loading knowledge base and embeddings...")
        
        # Set embeddings cache path
        self.embeddings_cache_path = Path.home() / "rag_robot_automation" / "data" / "embeddings.json"
        
        # Load and prepare data
        self._initialize_database(use_cached_embeddings)
        
        self.query_history = []
        
        print("\n" + "=" * 70)
        print("RAG Pipeline ready for queries!")
        print("=" * 70 + "\n")
    
    def _initialize_database(self, use_cached: bool = True):
        """Initialize vector database with embeddings"""
        
        if use_cached and self.embeddings_cache_path.exists():
            print("   - Loading cached embeddings...")
            embedded_chunks = self.embedder.load_embeddings(str(self.embeddings_cache_path))
        else:
            print("   - Generating embeddings from scratch...")
            chunks = self.retriever.get_all_chunks()
            embedded_chunks = self.embedder.embed_documents(chunks)
            self.embedder.save_embeddings(embedded_chunks, str(self.embeddings_cache_path))
        
        # Populate vector database
        self.vector_db.add_documents(embedded_chunks)
        
        # Print stats
        stats = self.vector_db.get_stats()
        print(f"   - Database ready: {stats['total_documents']} documents, "
              f"{stats['total_words']} words total")
    
    def query(self, user_query: str, top_k: int = 3) -> Dict:
        """Execute a complete RAG query"""
        
        print("\n" + "=" * 70)
        print(f"Query: {user_query}")
        print("=" * 70 + "\n")
        
        # Step 1: Embed the query
        print("Step 1: Embedding your query...")
        query_embedding = self.embedder.embed_text(user_query)
        print(f"✓ Query embedded to {len(query_embedding)} dimensions\n")
        
        # Step 2: Retrieve relevant documents
        print(f"Step 2: Retrieving top {top_k} relevant documents...")
        results = self.vector_db.search(query_embedding, top_k=top_k)
        print(f"✓ Found {len(results)} relevant documents:")
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['source']} (match: {result['similarity']:.1%})")
        
        # Step 3: Compile context
        print("\nStep 3: Compiling context from retrieved documents...")
        context = self._compile_context(results)
        print(f"✓ Context compiled: {len(context.split())} words\n")
        
        # Step 4: Generate response with LLM
        print("Step 4: Generating response with Ollama...")
        response = self.llm.generate(user_query, context)
        print("✓ Response generated\n")
        
        # Track query
        self.query_history.append({
            'query': user_query,
            'response': response,
            'context_docs': [r['source'] for r in results]
        })
        
        return {
            'query': user_query,
            'response': response,
            'retrieved_docs': results,
            'context': context
        }
    
    def _compile_context(self, results: List[Dict]) -> str:
        """Compile context from retrieved documents"""
        context_parts = []
        for result in results:
            context_parts.append(f"Source: {result['source']}\n{result['text']}")
        return "\n\n---\n\n".join(context_parts)
