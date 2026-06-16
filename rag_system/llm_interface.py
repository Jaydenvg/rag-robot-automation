import os
import requests
import json
from typing import Optional

class OllamaInterface:
    """Interface to Ollama for local LLM inference"""
    
    def __init__(self, model: str = "mistral", base_url: str = "http://localhost:11434"):
        """Initialize Ollama client"""
        self.model = model
        self.base_url = base_url
        self.conversation_history = []
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                print(f"Ollama connected successfully")
                print(f"Using model: {self.model}\n")
            else:
                raise ConnectionError("Ollama server not responding")
        except Exception as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}\n"
                f"Make sure Ollama is running: ollama serve"
            )
    
    def generate_response(self, user_query: str, context: str) -> str:
        """Generate response based on query and retrieved context"""
        
        # Build the prompt with context
        system_prompt = """You are an expert in robotics automation and control systems. 
You have access to a comprehensive knowledge base about safety protocols, control parameters, 
task specifications, troubleshooting, and best practices.

When answering questions:
1. Use the provided context to give accurate, practical answers
2. Be specific with numbers, parameters, and procedures
3. Prioritize safety considerations
4. If the context doesn't cover the question, say so clearly
5. Provide actionable guidance"""
        
        user_message = f"""Context from knowledge base:
{context}

User question: {user_query}

Please provide a detailed answer based on the knowledge base context."""
        
        try:
            print(f"Querying Ollama ({self.model})...")
            
            # Send request to Ollama
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": user_message,
                    "system": system_prompt,
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=120
            )
            
            if response.status_code != 200:
                return f"Error from Ollama: {response.text}"
            
            result = response.json()
            answer = result.get("response", "No response generated")
            
            # Track conversation
            self.conversation_history.append({
                "query": user_query,
                "context_used": len(context.split()),
                "response_length": len(answer.split())
            })
            
            return answer
        
        except requests.exceptions.ConnectionError:
            return (
                "Error: Cannot connect to Ollama. "
                "Make sure Ollama is running with: ollama serve"
            )
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_conversation_stats(self) -> dict:
        """Get statistics about conversation history"""
        if not self.conversation_history:
            return {"total_queries": 0}
        
        total_context_words = sum(h["context_used"] for h in self.conversation_history)
        total_response_words = sum(h["response_length"] for h in self.conversation_history)
        
        return {
            "total_queries": len(self.conversation_history),
            "total_context_words": total_context_words,
            "total_response_words": total_response_words,
            "avg_context_words": total_context_words / len(self.conversation_history),
            "avg_response_words": total_response_words / len(self.conversation_history)
        }

# For testing
if __name__ == "__main__":
    try:
        llm = OllamaInterface()
        
        # Test query
        test_context = """
        SAFETY PROTOCOLS:
        Maximum speed when humans are in the workspace is 0.5 meters per second.
        E-stop button should halt all motion immediately within 100 milliseconds.
        All personnel must wear safety glasses and closed-toe shoes.
        """
        
        test_query = "What safety precautions should I take when operating a robot near humans?"
        
        print(f"Test Query: {test_query}\n")
        print(f"Context provided: {len(test_context.split())} words\n")
        
        response = llm.generate_response(test_query, test_context)
        
        print("Response from Ollama:")
        print("-" * 50)
        print(response)
        print("-" * 50)
        
        stats = llm.get_conversation_stats()
        if stats['total_queries'] > 0:
            print(f"\nConversation Statistics:")
            print(f"  Total queries: {stats['total_queries']}")
            print(f"  Average context words: {stats['avg_context_words']:.1f}")
            print(f"  Average response words: {stats['avg_response_words']:.1f}")
        
    except Exception as e:
        print(f"Error: {e}")
