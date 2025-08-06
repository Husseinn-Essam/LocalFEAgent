"""
Configuration management for LFEA.
"""

import json
from pathlib import Path
from typing import Dict, List

class Config:
    """Configuration manager for LFEA settings."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._get_default_config_path()
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path."""
        return str(Path(__file__).parent / "default_config.json")
    
    def _load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
        except FileNotFoundError:
            config_data = self._get_default_config()
            self._save_config(config_data)
        
        # Set configuration attributes
        self.ollama_url = config_data.get("ollama_url", "http://localhost:11434")
        self.model_name = config_data.get("model_name", "gemma3n:e2b")
        self.capabilities = config_data.get("capabilities", ["search", "organize", "summarize", "chat"])
        self.file_categories = config_data.get("file_categories", self._get_default_categories())
    
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            "ollama_url": "http://localhost:11434",
            "model_name": "gemma3n:e2b",
            "capabilities": ["search", "organize", "summarize", "chat"],
            "file_categories": self._get_default_categories()
        }
    
    def _get_default_categories(self) -> Dict[str, List[str]]:
        """Get default file categories."""
        return {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
            'spreadsheets': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
            'presentations': ['.ppt', '.pptx', '.odp', '.key'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c', '.php', '.rb', '.go'],
            'executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage']
        }
    
    def _save_config(self, config_data: Dict):
        """Save configuration to file."""
        Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config_data, f, indent=2)
