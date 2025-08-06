import requests
from typing import Optional

class OllamaClient:
    """Client for communicating with Ollama API."""
    
    def __init__(self, url: str = "http://localhost:11434", model: str = "gemma3n:e2b"):
        self.url = url
        self.model = model
    
    def query(self, prompt: str, context_length: int = 1024, num_tokens: int = 150) -> str:
        """Send a query to Ollama API."""
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": context_length,
                        "num_predict": num_tokens,
                    }
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if Ollama API is available."""
        try:
            response = requests.get(f"{self.url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
