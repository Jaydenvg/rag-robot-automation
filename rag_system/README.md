# RAG Automation System

A complete Retrieval Augmented Generation (RAG) system for robotics automation that uses local LLM inference with Ollama for intelligent decision-making.

## Overview

This RAG system combines semantic search with language models to answer questions about robotics automation, control systems, safety protocols, troubleshooting, and best practices. All processing is done locally with zero API costs.

## Architecture

Knowledge Base (5 files)
         ↓
Document Retriever
         ↓

Chunks (17 pieces)
         ↓
Embedder (Sentence-Transformers)
         ↓
Embeddings (384-dimensional vectors)
         ↓
Vector Database
         ↓
User Query → Search → Top 3 Similar Chunks → Ollama LLM → Response


## Components

### 1. retriever.py
Loads knowledge base documents and splits them into overlapping chunks.

**Features:**
- Loads all `.txt` files from `data/knowledge_base/`
- Chunks documents into 400-word pieces with 50-word overlap
- Preserves sentence boundaries for context
- Returns metadata (source, word count, chunk ID)

**Usage:**
```python
from retriever import DocumentRetriever

retriever = DocumentRetriever()
documents = retriever.load_documents()
chunks = retriever.get_all_chunks()
```

### 2. embedder.py
Converts text chunks into semantic embeddings using Sentence-Transformers.

**Features:**
- Uses `all-MiniLM-L6-v2` model (lightweight, 384 dimensions)
- Generates embeddings for all chunks
- Caches embeddings to `data/embeddings.json`
- Supports embedding similarity calculations

**Usage:**
```python
from embedder import DocumentEmbedder

embedder = DocumentEmbedder()
embedded_chunks = embedder.embed_documents(chunks)
embedder.save_embeddings(embedded_chunks)
```

### 3. vector_db.py
Stores embeddings and performs semantic similarity search.

**Features:**
- Implements cosine similarity search
- Returns top-k most similar documents
- Provides database statistics
- Stores 17 documents (4,936 words total)

**Usage:**
```python
from vector_db import VectorDatabase

db = VectorDatabase()
db.add_documents(embedded_chunks)
results = db.search(query_embedding, top_k=3)
```

### 4. llm_interface.py
Manages communication with Ollama for response generation.

**Features:**
- Connects to local Ollama server (localhost:11434)
- Uses Mistral 7B model
- Handles error checking and connection verification
- Tracks conversation statistics

**Usage:**
```python
from llm_interface import OllamaInterface

llm = OllamaInterface(model="mistral")
response = llm.generate_response(query, context)
```

### 5. rag_pipeline.py
Orchestrates all components into a complete RAG system.

**Features:**
- Initializes all components
- Executes complete query workflow
- Maintains query history
- Provides formatted output display
- Generates system statistics

**Usage:**
```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
result = rag.query("What is the maximum safe robot speed?")
rag.display_result(result)
```

### 6. interactive_rag.py
Interactive command-line chatbot interface.

**Features:**
- Real-time query processing
- Special commands (quit, stats, help, clear)
- Conversation history
- System statistics display

**Commands:**
- `quit` - Exit the chatbot
- `stats` - Show system statistics
- `help` - Show help message
- `clear` - Clear conversation history

### 7. test_rag_system.py
Comprehensive automated testing suite.

**Features:**
- Tests all major automation domains
- Validates response quality
- Measures query response times
- Generates test statistics

## Installation

### Prerequisites
- Python 3.10+
- Ollama installed and running
- Mistral 7B model downloaded

### Setup Steps

1. **Install Ollama:**
```bash
   # Download from https://ollama.ai
   # Or on Ubuntu:
   curl -fsSL https://ollama.ai/install.sh | sh
```

2. **Download Mistral Model:**
```bash
   ollama pull mistral
```

3. **Install Python Dependencies:**
```bash
   pip install sentence-transformers numpy requests
```

4. **Start Ollama Server:**
```bash
   # In a separate terminal
   ollama serve
```

## Usage

### Start Interactive Chatbot

```bash
python3 interactive_rag.py
```

Then ask questions:

You: What safety precautions should I follow when operating a robot near humans?

Ollama:

[Generates response based on safety protocols from knowledge base]


### Run Tests

```bash
python3 test_rag_system.py
```

Output:

Test 1: Safety

Query: What is the maximum safe robot speed near humans?

✓ PASSED (15.3s)

Found keywords: speed, meters, humans


### Use Programmatically

```python
from rag_pipeline import RAGPipeline

# Initialize RAG system
rag = RAGPipeline(use_cached_embeddings=True, model="mistral")

# Run query
result = rag.query("How do I tune a PID controller?")

# Display result
rag.display_result(result)

# Get statistics
stats = rag.get_stats()
print(f"Queries processed: {stats['total_queries']}")
```

## System Specifications

| Metric               | Value            |
|----------------------|------------------|
| Knowledge base files | 5                |
| Document chunks      | 17               |
| Total words in DB    | 4,936            |
| Embedding dimension  | 384              |
| Embedding model      | all-MiniLM-L6-v2 |
| LLM model            | Mistral 7B       |
| Query response time  | 10-30 seconds    |
| API cost             | $0 (fully local) |

## Performance

### Query Coverage
- **Safety Protocols**: Successfully retrieves safety guidelines and limits
- **Control Systems**: Accurately finds PID parameters and tuning procedures
- **Task Operations**: Returns detailed task specifications
- **Troubleshooting**: Provides diagnostic and repair procedures
- **Best Practices**: Offers optimization and maintenance guidance

### Response Quality
- Retrieves 3 most relevant documents per query
- Generates contextual responses using retrieved documents
- Maintains conversation history
- Tracks query statistics

## Troubleshooting

### "Cannot connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check server is listening on localhost:11434
- Verify network connectivity

### "Model not found"
- Download Mistral: `ollama pull mistral`
- List available models: `ollama list`

### Slow Response Times
- First query is slower due to model initialization
- Subsequent queries are faster
- Response time depends on hardware (CPU/GPU)

### Out of Memory
- Reduce model size: Use `ollama pull neural-chat` (smaller)
- Close other applications
- Increase available RAM

## File Structure

rag_system/

├── init.py

├── retriever.py           # Document loading and chunking

├── embedder.py            # Embedding generation

├── vector_db.py           # Vector database and search

├── llm_interface.py       # Ollama LLM integration

├── rag_pipeline.py        # Main RAG pipeline

├── interactive_rag.py     # Interactive chatbot

├── test_rag_system.py     # Test suite

└── README.md              # This file
data/

├── knowledge_base/        # Knowledge base documents

│   ├── safety_protocols.txt

│   ├── control_system_parameters.txt

│   ├── task_specifications.txt

│   ├── troubleshooting_guide.txt

│   └── best_practices.txt

├── embeddings.json        # Cached embeddings

└── chroma_db/            # Vector database (future)


## Integration with ROS2

The RAG system is designed to integrate with ROS2:

```python
# Future Phase 4
from rag_pipeline import RAGPipeline
import rclpy

class RAGQueryServer(Node):
    def __init__(self):
        super().__init__('rag_query_server')
        self.rag = RAGPipeline()
        
    def handle_query(self, request):
        result = self.rag.query(request.query)
        return result.response
```

## Cost Analysis

| Option           | Cost           | Speed     | Local |
|------------------|----------------|-----------|-------|
| Claude API       | $5-50+/month   | 2-5 sec   | No    |
| OpenAI API       | $10-100+/month | 1-3 sec   | No    |
| Ollama (Mistral) | $0             | 10-30 sec | Yes ✓ |

## Future Enhancements

- [ ] GPU acceleration with CUDA
- [ ] Vector database optimization (Chroma, Pinecone)
- [ ] Multi-model support
- [ ] Fine-tuning on automation domain
- [ ] Conversation memory
- [ ] Confidence scoring
- [ ] Citation tracking
- [ ] ROS2 service node integration

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Test your changes with `test_rag_system.py`
2. Update documentation
3. Commit with clear messages
4. Push to GitHub

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review system logs
3. Run test suite: `python3 test_rag_system.py`
4. Check GitHub issues

## Contact

GitHub: https://github.com/Jaydenvg/rag-robot-automation
