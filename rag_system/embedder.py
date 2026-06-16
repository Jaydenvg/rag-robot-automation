from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import json
import os

class DocumentEmbedder:
    """Generates embeddings for document chunks"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = 384  # Dimension of all-MiniLM-L6-v2
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}\n")
    
    def embed_text(self, text: str) -> np.ndarray:
        """Convert single text to embedding"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding
    
    def embed_documents(self, chunks: List[Dict[str, str]]) -> List[Dict]:
        """Generate embeddings for all document chunks"""
        print(f"Generating embeddings for {len(chunks)} chunks...")
        
        embedded_chunks = []
        
        for i, chunk in enumerate(chunks):
            if (i + 1) % 10 == 0:
                print(f"  Processing chunk {i + 1}/{len(chunks)}")
            
            embedding = self.embed_text(chunk['text'])
            
            embedded_chunks.append({
                'id': chunk['id'],
                'text': chunk['text'],
                'source': chunk['source'],
                'embedding': embedding.tolist(),  # Convert to list for storage
                'word_count': chunk['word_count']
            })
        
        print(f"Generated {len(embedded_chunks)} embeddings\n")
        return embedded_chunks
    
    def save_embeddings(self, embedded_chunks: List[Dict], filepath: str = "data/embeddings.json"):
        """Save embeddings to file for later use"""
        print(f"Saving embeddings to {filepath}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(embedded_chunks, f)
        
        print(f"Embeddings saved successfully\n")
    
    def load_embeddings(self, filepath: str = "data/embeddings.json") -> List[Dict]:
        """Load previously generated embeddings"""
        print(f"Loading embeddings from {filepath}")
        
        with open(filepath, 'r') as f:
            embedded_chunks = json.load(f)
        
        print(f"Loaded {len(embedded_chunks)} embeddings\n")
        return embedded_chunks
    
    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# For testing
if __name__ == "__main__":
    from retriever import DocumentRetriever
    
    retriever = DocumentRetriever()
    chunks = retriever.get_all_chunks()
    
    embedder = DocumentEmbedder()
    embedded_chunks = embedder.embed_documents(chunks)
    
    # Save embeddings
    embedder.save_embeddings(embedded_chunks)
    
    print("Sample embedding info:")
    chunk = embedded_chunks[0]
    print(f"Chunk {chunk['id']}: {chunk['text'][:100]}...")
    print(f"Embedding dimension: {len(chunk['embedding'])}")
    print(f"First 5 values: {chunk['embedding'][:5]}")

