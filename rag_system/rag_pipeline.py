import os
from typing import List, Dict
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
        # Load and prepare data
        self._initialize_database(use_cached_embeddings)
        
        self.query_history = []
        
        print("\n" + "=" * 70)
        print("RAG Pipeline ready for queries!")
        print("=" * 70 + "\n")
    
    def _initialize_database(self, use_cached: bool = True):
        """Initialize vector database with embeddings"""
        embeddings_file = "data/embeddings.json"
        
        if use_cached and os.path.exists(embeddings_file):
            print("   - Loading cached embeddings...")
            embedded_chunks = self.embedder.load_embeddings(embeddings_file)
        else:
            print("   - Generating embeddings from scratch...")
            chunks = self.retriever.get_all_chunks()
            embedded_chunks = self.embedder.embed_documents(chunks)
            self.embedder.save_embeddings(embedded_chunks)
        
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
        retrieved_docs = self.vector_db.search(query_embedding, top_k=top_k)
        
        if retrieved_docs:
            print(f"✓ Found {len(retrieved_docs)} relevant documents:")
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"   {i}. {doc['source']} (match: {doc['similarity_score']*100:.1f}%)")
        else:
            print("✗ No relevant documents found")
        print()
        
        # Step 3: Compile context from retrieved documents
        print("Step 3: Compiling context from retrieved documents...")
        context = self._compile_context(retrieved_docs)
        context_words = len(context.split())
        print(f"✓ Context compiled: {context_words} words\n")
        
        # Step 4: Generate response with Ollama
        print("Step 4: Generating response with Ollama...")
        print("(This may take 10-30 seconds for the first query)\n")
        response = self.llm.generate_response(user_query, context)
        print("✓ Response generated\n")
        
        # Store in history
        result = {
            "query": user_query,
            "retrieved_documents": retrieved_docs,
            "context_length": context_words,
            "response": response,
            "context": context
        }
        
        self.query_history.append(result)
        
        return result
    
    def _compile_context(self, documents: List[Dict]) -> str:
        """Compile retrieved documents into context string"""
        if not documents:
            return "No relevant documents found in knowledge base."
        
        context_parts = []
        
        for doc in documents:
            source = doc['source'].replace('.txt', '').replace('_', ' ').title()
            context_parts.append(f"From {source}:\n{doc['text']}\n")
        
        return "\n---\n".join(context_parts)
    
    def display_result(self, result: Dict):
        """Pretty print a query result"""
        print("\n" + "=" * 70)
        print("RESPONSE FROM OLLAMA")
        print("=" * 70)
        print(result['response'])
        print("\n" + "=" * 70)
        print("SOURCES USED")
        print("=" * 70)
        
        sources_seen = set()
        if result['retrieved_documents']:
            for doc in result['retrieved_documents']:
                if doc['source'] not in sources_seen:
                    similarity = doc['similarity_score'] * 100
                    print(f"• {doc['source']} ({similarity:.1f}% match)")
                    sources_seen.add(doc['source'])
        else:
            print("No sources retrieved")
        
        print(f"\nContext size: {result['context_length']} words")
        print("=" * 70 + "\n")
    
    def get_stats(self) -> Dict:
        """Get pipeline statistics"""
        if not self.query_history:
            return {
                "total_queries": 0,
                "documents_in_db": self.vector_db.get_stats()["total_documents"],
                "embedding_dimension": self.vector_db.get_stats()["embedding_dimension"]
            }
        
        return {
            "total_queries": len(self.query_history),
            "total_context_words": sum(q["context_length"] for q in self.query_history),
            "avg_context_words": sum(q["context_length"] for q in self.query_history) / len(self.query_history),
            "documents_in_db": self.vector_db.get_stats()["total_documents"],
            "embedding_dimension": self.vector_db.get_stats()["embedding_dimension"],
            "llm_model": self.llm.model
        }

# For automated testing
def run_test_queries():
    """Run example queries to test the system"""
    try:
        rag = RAGPipeline(use_cached_embeddings=True, model="mistral")
        
        # Example queries covering different domains
        test_queries = [
            "What is the maximum safe speed for a robot operating near humans?",
            "How should I tune a PID controller for position control?",
            "What are the steps for a basic pick and place operation?",
            "What should I do if a motor stops responding to commands?",
        ]
        
        print("\n" + "=" * 70)
        print("RUNNING TEST QUERIES")
        print("=" * 70)
        
        for i, query in enumerate(test_queries[:2], 1):  # Run first 2 queries
            print(f"\n{'='*70}")
            print(f"TEST QUERY {i}/{len(test_queries)}")
            print(f"{'='*70}\n")
            
            result = rag.query(query)
            rag.display_result(result)
        
        # Print final statistics
        print("\n" + "=" * 70)
        print("PIPELINE STATISTICS")
        print("=" * 70)
        stats = rag.get_stats()
        print(f"Queries processed: {stats['total_queries']}")
        print(f"Documents in DB: {stats['documents_in_db']}")
        print(f"Embedding dimension: {stats['embedding_dimension']}")
        print(f"LLM Model: {stats['llm_model']}")
        print(f"Total context words used: {stats['total_context_words']}")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

# For testing
if __name__ == "__main__":
    run_test_queries()
