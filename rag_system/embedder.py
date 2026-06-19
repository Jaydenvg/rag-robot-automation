"""Embedder - Converts text to embeddings"""

from sentence_transformers import SentenceTransformer
from typing import List, Dict
import json
from pathlib import Path


class DocumentEmbedder:
    """Converts documents to embeddings using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedder with specified model"""
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def embed_text(self, text: str) -> List[float]:
        """Convert a single text string to embedding"""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def embed_documents(self, chunks: List[Dict]) -> List[Dict]:
        """Embed a list of document chunks"""
        embedded_chunks = []
        
        for idx, chunk in enumerate(chunks):
            embedding = self.embed_text(chunk['text'])
            embedded_chunks.append({
                'id': chunk.get('id', f"chunk_{idx}"),
                'text': chunk['text'],
                'source': chunk.get('source', 'unknown'),
                'embedding': embedding
            })
        
        return embedded_chunks
    
    def save_embeddings(self, embedded_chunks: List[Dict], filepath: str):
        """Save embeddings to JSON file"""
        # Convert embeddings to lists for JSON serialization
        data = []
        for chunk in embedded_chunks:
            data.append({
                'id': chunk['id'],
                'text': chunk['text'],
                'source': chunk['source'],
                'embedding': chunk['embedding']
            })
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f)
        print(f"Saved {len(data)} embeddings to {filepath}")
    
    def load_embeddings(self, filepath: str) -> List[Dict]:
        """Load embeddings from JSON file"""
        if not Path(filepath).exists():
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        print(f"Loaded {len(data)} embeddings")
        return data
    
    def get_embedding_dimension(self) -> int:
        """Get embedding dimension"""
        return self.embedding_dim
