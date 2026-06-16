import os
from pathlib import Path
from typing import List, Dict
import re

class DocumentRetriever:
    """Loads and chunks knowledge base documents"""
    
    def __init__(self, kb_path: str = "data/knowledge_base"):
        self.kb_path = Path(kb_path)
        self.chunk_size = 400
        self.chunk_overlap = 50
        self.documents = []
        
    def load_documents(self) -> List[Dict[str, str]]:
        """Load all text files from knowledge base directory"""
        print(f"Loading documents from {self.kb_path}...")
        
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base path not found: {self.kb_path}")
        
        documents = []
        txt_files = list(self.kb_path.glob("*.txt"))
        
        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in {self.kb_path}")
        
        for file_path in sorted(txt_files):
            print(f"  - Loading {file_path.name}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            documents.append({
                'filename': file_path.name,
                'content': content
            })
        
        self.documents = documents
        print(f"Loaded {len(documents)} documents\n")
        return documents
    
    def chunk_document(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        """Split a document into overlapping chunks"""
        if chunk_size is None:
            chunk_size = self.chunk_size
        if overlap is None:
            overlap = self.chunk_overlap
        
        # Split by sentences to keep context together
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            if current_size + sentence_words > chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append(chunk_text)
                
                # Start new chunk with overlap
                overlap_sentences = []
                overlap_size = 0
                for s in reversed(current_chunk):
                    s_words = len(s.split())
                    if overlap_size + s_words <= overlap:
                        overlap_sentences.insert(0, s)
                        overlap_size += s_words
                    else:
                        break
                
                current_chunk = overlap_sentences + [sentence]
                current_size = overlap_size + sentence_words
            else:
                current_chunk.append(sentence)
                current_size += sentence_words
        
        # Add final chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def get_all_chunks(self) -> List[Dict[str, str]]:
        """Get all documents as chunks with metadata"""
        if not self.documents:
            self.load_documents()
        
        all_chunks = []
        chunk_id = 0
        
        for doc in self.documents:
            filename = doc['filename']
            content = doc['content']
            
            chunks = self.chunk_document(content)
            
            for chunk_text in chunks:
                all_chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'source': filename,
                    'word_count': len(chunk_text.split())
                })
                chunk_id += 1
        
        print(f"Created {len(all_chunks)} chunks from {len(self.documents)} documents\n")
        return all_chunks

# For testing
if __name__ == "__main__":
    retriever = DocumentRetriever()
    documents = retriever.load_documents()
    chunks = retriever.get_all_chunks()
    
    print("Sample chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {chunk['id']} (from {chunk['source']}):")
        print(f"Words: {chunk['word_count']}")
        print(f"Text: {chunk['text'][:200]}...")
