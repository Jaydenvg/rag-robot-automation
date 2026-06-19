"""Document Retriever - Loads and manages knowledge base documents"""

from pathlib import Path
from typing import List, Dict


class DocumentRetriever:
    """Retrieves documents from knowledge base"""
    
    def __init__(self):
        """Initialize document retriever with knowledge base path"""
        self.kb_path = Path.home() / "rag_robot_automation" / "data" / "knowledge_base"
        self.documents = []
        self.load_documents()
    
    def load_documents(self):
        """Load all documents from knowledge base directory"""
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base path not found: {self.kb_path}")
        
        self.documents = []
        txt_files = sorted(self.kb_path.glob("*.txt"))
        
        for file_path in txt_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.documents.append({
                    'filename': file_path.stem,
                    'content': content,
                    'path': str(file_path)
                })
    
    def get_documents(self) -> List[Dict]:
        """Get all loaded documents"""
        return self.documents
    
    def get_document_by_name(self, name: str) -> Dict:
        """Get a specific document by filename"""
        for doc in self.documents:
            if doc['filename'] == name:
                return doc
        return None
    
    def get_all_chunks(self) -> List[Dict]:
        """Get all documents as chunks"""
        chunks = []
        for doc in self.documents:
            chunks.append({
                'text': doc['content'],
                'source': doc['filename'],
                'path': doc['path']
            })
        return chunks
    
    def search_documents(self, keywords: List[str]) -> List[Dict]:
        """Simple keyword search across documents"""
        results = []
        for doc in self.documents:
            score = 0
            for keyword in keywords:
                if keyword.lower() in doc['content'].lower():
                    score += doc['content'].lower().count(keyword.lower())
            
            if score > 0:
                results.append({
                    'filename': doc['filename'],
                    'content': doc['content'],
                    'relevance_score': score
                })
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
