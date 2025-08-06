from typing import List, Dict, Any
from pathlib import Path

from .llm.ollama_client import OllamaClient
from .core.file_manager import FileManager
from .core.intent_detector import IntentDetector
from .core.content_analyzer import ContentAnalyzer
from .config.settings import Config

class LFEAgent:
    """Main agent class that provides high-level interface to all functionality."""
    
    def __init__(self, config_path: str = None):
        self.config = Config(config_path)
        self.llm_client = OllamaClient(
            url=self.config.ollama_url,
            model=self.config.model_name
        )
        self.file_manager = FileManager(self.config.file_categories)
        self.intent_detector = IntentDetector(self.llm_client, self.config.capabilities)
        self.content_analyzer = ContentAnalyzer(self.llm_client)
    
    def search_files_by_content(self, directory: str, query: str) -> List[Dict[str, Any]]:
        """Search files in directory by content using AI analysis."""
        return self.content_analyzer.search_files_by_content(directory, query)
    
    def organize_files_by_content(self, directory: str) -> Dict[str, Any]:
        """Organize files in directory based on content analysis."""
        return self.content_analyzer.organize_files_by_content(directory)
    
    def detect_intent(self, query: str) -> str:
        """Detect user intent from query."""
        return self.intent_detector.detect_intent(query)
    
    def chat(self, message: str) -> str:
        """Chat with the AI agent."""
        return self.llm_client.query(message, context_length=1024, num_tokens=200)
    
    def get_capabilities(self) -> List[str]:
        """Get list of agent capabilities."""
        return self.config.capabilities
