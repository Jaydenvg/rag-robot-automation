"""
RAG System Configuration
Centralized configuration for all RAG system components
"""

import os
from pathlib import Path

# ============================================================================
# PATHS CONFIGURATION
# ============================================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = DATA_DIR / "knowledge_base"
EMBEDDINGS_FILE = DATA_DIR / "embeddings.json"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"

# Create directories if they don't exist
KB_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# DOCUMENT RETRIEVER CONFIGURATION
# ============================================================================

RETRIEVER_CONFIG = {
    # Knowledge base path
    "kb_path": str(KB_DIR),
    
    # Chunk size in words (approximate)
    "chunk_size": 400,
    
    # Overlap between chunks in words
    "chunk_overlap": 50,
    
    # File extensions to process
    "file_extensions": [".txt"],
}

# ============================================================================
# EMBEDDER CONFIGURATION
# ============================================================================

EMBEDDER_CONFIG = {
    # Model name for Sentence-Transformers
    "model_name": "all-MiniLM-L6-v2",
    
    # Expected embedding dimension (fixed for all-MiniLM-L6-v2)
    "embedding_dim": 384,
    
    # Path to save/load embeddings
    "embeddings_file": str(EMBEDDINGS_FILE),
    
    # Whether to use GPU if available
    "use_gpu": True,
    
    # Batch size for embedding generation
    "batch_size": 32,
}

# ============================================================================
# VECTOR DATABASE CONFIGURATION
# ============================================================================

VECTOR_DB_CONFIG = {
    # Number of top results to return for search
    "default_top_k": 3,
    
    # Minimum similarity threshold (0.0 to 1.0)
    "similarity_threshold": 0.0,
    
    # Database type (simple, chroma, pinecone)
    "db_type": "simple",
    
    # Chroma database path (for future enhancement)
    "chroma_path": str(CHROMA_DB_DIR),
    
    # Chroma collection name
    "collection_name": "robotics_knowledge",
}

# ============================================================================
# OLLAMA LLM CONFIGURATION
# ============================================================================

OLLAMA_CONFIG = {
    # Ollama server host
    "host": "localhost",
    
    # Ollama server port
    "port": 11434,
    
    # Base URL for API calls
    "base_url": "http://localhost:11434",
    
    # Model to use for inference
    "model": "mistral",
    
    # Alternative models: neural-chat, llama2, dolphin-mixtral, etc.
    "alternative_models": [
        "neural-chat",  # Smaller, faster
        "llama2",       # Larger, slower but better quality
        "dolphin-mixtral",  # Fast and capable
    ],
    
    # Temperature for response generation (0.0 to 1.0)
    "temperature": 0.7,
    
    # Maximum tokens in response
    "max_tokens": 1024,
    
    # Request timeout in seconds
    "timeout": 120,
    
    # Number of retries for failed requests
    "max_retries": 3,
}

# ============================================================================
# RAG PIPELINE CONFIGURATION
# ============================================================================

RAG_CONFIG = {
    # Use cached embeddings if available
    "use_cached_embeddings": True,
    
    # Number of documents to retrieve
    "retrieval_top_k": 3,
    
    # Whether to show detailed logging
    "verbose": True,
    
    # RAG system model (Ollama model name)
    "model": "mistral",
}

# ============================================================================
# INTERACTIVE CHATBOT CONFIGURATION
# ============================================================================

CHATBOT_CONFIG = {
    # System prompt for the chatbot
    "system_prompt": """You are an expert in robotics automation and control systems. 
You have access to a comprehensive knowledge base about safety protocols, control parameters, 
task specifications, troubleshooting, and best practices.

When answering questions:
1. Use the provided context to give accurate, practical answers
2. Be specific with numbers, parameters, and procedures
3. Prioritize safety considerations
4. If the context doesn't cover the question, say so clearly
5. Provide actionable guidance""",
    
    # Welcome message
    "welcome_message": "Welcome to RAG Automation Chatbot! Ask me anything about robotics.",
    
    # Help text
    "help_text": """Commands:
  'quit'  - Exit the chatbot
  'stats' - Show system statistics
  'help'  - Show this help message
  'clear' - Clear conversation history

Or just type your question about robotics and automation!""",
}

# ============================================================================
# TESTING CONFIGURATION
# ============================================================================

TEST_CONFIG = {
    # Test queries organized by category
    "test_queries": [
        {
            "category": "Safety",
            "query": "What is the maximum safe robot speed near humans?",
            "expected_keywords": ["speed", "meters", "humans", "0.5"]
        },
        {
            "category": "Control Systems",
            "query": "How do I tune PID controller parameters?",
            "expected_keywords": ["PID", "Kp", "Ki", "Kd", "proportional"]
        },
        {
            "category": "Task Operations",
            "query": "What are the steps for pick and place operation?",
            "expected_keywords": ["gripper", "approach", "placement", "release"]
        },
        {
            "category": "Troubleshooting",
            "query": "What should I do if a sensor is not working?",
            "expected_keywords": ["check", "verify", "connection", "power"]
        },
        {
            "category": "Best Practices",
            "query": "What is important for preventive maintenance?",
            "expected_keywords": ["maintenance", "check", "lubricate", "inspect"]
        }
    ],
    
    # Minimum keyword matches to pass test
    "min_keyword_matches": 1,
    
    # Show detailed test output
    "verbose": True,
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    "level": "INFO",
    
    # Log file path
    "log_file": PROJECT_ROOT / "logs" / "rag_system.log",
    
    # Log format
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    
    # Create logs directory if it doesn't exist
    "create_log_dir": True,
}

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

PERFORMANCE_CONFIG = {
    # Cache embeddings in memory after first load
    "cache_embeddings": True,
    
    # Number of worker threads for embeddings
    "num_workers": 4,
    
    # Preload vector database on startup
    "preload_vector_db": True,
    
    # Enable query result caching (for identical queries)
    "enable_result_cache": False,
    
    # Cache size (number of results to keep)
    "cache_size": 100,
}

# ============================================================================
# VALIDATION AND UTILITY FUNCTIONS
# ============================================================================

def validate_config():
    """Validate configuration settings"""
    issues = []
    
    # Check required directories exist
    if not KB_DIR.exists():
        issues.append(f"Knowledge base directory not found: {KB_DIR}")
    
    if not DATA_DIR.exists():
        issues.append(f"Data directory not found: {DATA_DIR}")
    
    # Check embeddings file
    if not EMBEDDINGS_FILE.exists():
        print(f"Warning: Embeddings file not found: {EMBEDDINGS_FILE}")
        print("System will generate embeddings on first run.")
    
    # Check Ollama connectivity
    try:
        import requests
        response = requests.get(
            f"{OLLAMA_CONFIG['base_url']}/api/tags",
            timeout=5
        )
        if response.status_code != 200:
            issues.append("Ollama server not responding")
    except Exception as e:
        issues.append(f"Cannot connect to Ollama: {str(e)}")
    
    return issues

def print_config_summary():
    """Print configuration summary"""
    print("\n" + "=" * 70)
    print("RAG SYSTEM CONFIGURATION")
    print("=" * 70)
    
    print("\nPaths:")
    print(f"  Project root: {PROJECT_ROOT}")
    print(f"  Knowledge base: {KB_DIR}")
    print(f"  Embeddings: {EMBEDDINGS_FILE}")
    
    print("\nDocument Retriever:")
    print(f"  Chunk size: {RETRIEVER_CONFIG['chunk_size']} words")
    print(f"  Chunk overlap: {RETRIEVER_CONFIG['chunk_overlap']} words")
    
    print("\nEmbedder:")
    print(f"  Model: {EMBEDDER_CONFIG['model_name']}")
    print(f"  Dimensions: {EMBEDDER_CONFIG['embedding_dim']}")
    
    print("\nVector Database:")
    print(f"  Default top-k: {VECTOR_DB_CONFIG['default_top_k']}")
    print(f"  Type: {VECTOR_DB_CONFIG['db_type']}")
    
    print("\nOllama LLM:")
    print(f"  Server: {OLLAMA_CONFIG['base_url']}")
    print(f"  Model: {OLLAMA_CONFIG['model']}")
    print(f"  Temperature: {OLLAMA_CONFIG['temperature']}")
    
    print("\n" + "=" * 70 + "\n")

# Run validation on import
if __name__ == "__main__":
    print_config_summary()
    issues = validate_config()
    if issues:
        print("Configuration Issues:")
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("✓ Configuration is valid\n")
