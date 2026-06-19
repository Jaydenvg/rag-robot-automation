"""LLM Interface - Handles communication with Ollama"""

import requests
from typing import Dict, List


class OllamaInterface:
    """Interface for Ollama LLM"""
    
    def __init__(self, model: str = "mistral", host: str = "localhost", port: int = 11434):
        """Initialize Ollama interface"""
        self.model = model
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        
        # Test connection
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                print("Ollama connected successfully")
                print(f"Using model: {model}")
            else:
                raise Exception("Failed to connect to Ollama")
        except Exception as e:
            raise Exception(f"Cannot connect to Ollama at {self.base_url}: {e}")
    
    def generate(self, prompt: str, context: str = "", max_tokens: int = 500) -> str:
        """Generate response using Ollama"""
        
        # Combine prompt and context
        full_prompt = f"""Based on the following context, answer the question concisely:

Context:
{context}

Question: {prompt}

Answer:"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False,
                    "num_predict": max_tokens
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"Error: Ollama returned status {response.status_code}"
        
        except requests.exceptions.Timeout:
            return "Error: Ollama request timed out"
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    
    def extract_command(self, response: str) -> Dict:
        """Extract robot command from response"""
        response_lower = response.lower()
        
        command = {
            'action': 'idle',
            'speed': 0.0,
            'angular': 0.0
        }
        
        # Check for speed values
        if any(word in response_lower for word in ['0.5', 'safe', 'maximum', 'normal']):
            command['action'] = 'move'
            command['speed'] = 0.5
        elif any(word in response_lower for word in ['0.2', 'slow', 'caution', 'careful']):
            command['action'] = 'move'
            command['speed'] = 0.2
        elif any(word in response_lower for word in ['1.0', 'fast', 'accelerate', 'quickly']):
            command['action'] = 'move'
            command['speed'] = 1.0
        elif any(word in response_lower for word in ['stop', 'halt', 'emergency']):
            command['action'] = 'stop'
            command['speed'] = 0.0
        
        # Check for rotation
        if 'left' in response_lower:
            command['angular'] = 0.5
        elif 'right' in response_lower:
            command['angular'] = -0.5
        
        return command
