import json
import numpy as np
from typing import List, Dict


class VectorDatabase:
    """Simple vector database for storing and searching embeddings"""
    
    def __init__(self):
        self.embeddings = []
        self.index = {}
    
    def add_documents(self, embedded_chunks: List[Dict]):
        """Add embedded documents to the database"""
        print(f"Adding {len(embedded_chunks)} documents to vector database...")
        
        for chunk in embedded_chunks:
            word_count = len(chunk['text'].split())
            self.embeddings.append({
                'id': chunk['id'],
                'text': chunk['text'],
                'source': chunk['source'],
                'embedding': np.array(chunk['embedding']),
                'word_count': word_count
            })
            
            self.index[chunk['id']] = len(self.embeddings) - 1
        
        print(f"Database now contains {len(self.embeddings)} documents\n")
    
    def search(self, query_embedding, top_k: int = 3) -> List[Dict]:
        """Search for most similar documents using cosine similarity"""
        if not self.embeddings:
            return []
        
        # Convert query embedding to numpy array if needed
        if isinstance(query_embedding, list):
            query_embedding = np.array(query_embedding)
        
        similarities = []
        
        for i, doc in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc['embedding'])
            similarities.append((i, similarity, doc))
        
        # Sort by similarity and get top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:top_k]
        
        results = []
        for idx, score, doc in top_results:
            results.append({
                'id': doc['id'],
                'text': doc['text'],
                'source': doc['source'],
                'similarity': float(score),
                'word_count': doc['word_count']
            })
        
        return results
    
    @staticmethod
    def _cosine_similarity(a, b) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(a) if not isinstance(a, np.ndarray) else a
        b = np.array(b) if not isinstance(b, np.ndarray) else b
        
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0
        
        return float(dot_product / (norm_a * norm_b))
    
    def get_document(self, doc_id: str) -> Dict:
        """Get a document by ID"""
        if doc_id not in self.index:
            return None
        
        idx = self.index[doc_id]
        doc = self.embeddings[idx]
        
        return {
            'id': doc['id'],
            'text': doc['text'],
            'source': doc['source'],
            'word_count': doc['word_count']
        }
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        total_words = sum(doc['word_count'] for doc in self.embeddings)
        
        return {
            'total_documents': len(self.embeddings),
            'total_words': total_words,
            'average_doc_length': total_words / len(self.embeddings) if self.embeddings else 0,
            'embedding_dimension': len(self.embeddings[0]['embedding']) if self.embeddings else 0
        }
