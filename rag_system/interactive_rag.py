from rag_pipeline import RAGPipeline
import sys

def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  RAG AUTOMATION CHATBOT".center(68) + "║")
    print("║" + "  Powered by Ollama + Robotics Knowledge Base".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print("=" * 70 + "\n")

def print_help():
    """Print help message"""
    print("\nCommands:")
    print("  'quit'  - Exit the chatbot")
    print("  'stats' - Show system statistics")
    print("  'help'  - Show this help message")
    print("  'clear' - Clear conversation history")
    print("\nOr just type your question about robotics and automation!\n")

def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize RAG pipeline
    print("Initializing RAG system with Ollama...")
    print("(Make sure 'ollama serve' is running in another terminal)\n")
    
    try:
        rag = RAGPipeline(use_cached_embeddings=True, model="mistral")
    except Exception as e:
        print(f"\nError initializing RAG system:")
        print(f"{e}\n")
        print("Make sure:")
        print("1. Ollama is installed: https://ollama.ai")
        print("2. Mistral model is downloaded: ollama pull mistral")
        print("3. Ollama server is running: ollama serve")
        return
    
    print_help()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == 'quit':
                print("\nGoodbye! Thanks for using RAG Automation Chatbot.\n")
                break
            
            elif user_input.lower() == 'help':
                print_help()
                continue
            
            elif user_input.lower() == 'stats':
                print_statistics(rag)
                continue
            
            elif user_input.lower() == 'clear':
                rag.query_history = []
                print("\nConversation history cleared.\n")
                continue
            
            # Process query
            print()
            result = rag.query(user_input)
            
            # Display response
            print("\nOllama:")
            print("-" * 70)
            print(result['response'])
            print("-" * 70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.\n")
            continue
        except Exception as e:
            print(f"\nError processing query: {e}\n")

def print_statistics(rag):
    """Print pipeline statistics"""
    stats = rag.get_stats()
    
    print("\n" + "=" * 70)
    print("PIPELINE STATISTICS")
    print("=" * 70)
    print(f"Queries processed: {stats['total_queries']}")
    print(f"Documents in database: {stats['documents_in_db']}")
    print(f"Embedding dimension: {stats['embedding_dimension']}")
    print(f"LLM Model: {stats['llm_model']}")
    
    if stats['total_queries'] > 0:
        print(f"Total context words used: {stats['total_context_words']}")
        print(f"Average context per query: {stats['avg_context_words']:.1f} words")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
