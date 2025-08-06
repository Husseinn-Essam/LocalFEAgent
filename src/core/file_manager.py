"""
File management utilities and helpers.
"""

import os
from pathlib import Path
from typing import Dict, List

class FileManager:
    """Manages file operations and categorization."""
    
    def __init__(self, file_categories: Dict[str, List[str]]):
        self.file_categories = file_categories
    
    def get_file_category(self, file_path: str) -> str:
        """Get the category of a file based on its extension."""
        extension = Path(file_path).suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if extension in extensions:
                return category
        
        return "unknown"
    
    def is_document(self, file_path: str) -> bool:
        """Check if file is a document type."""
        extension = Path(file_path).suffix.lower()
        return extension in self.file_categories.get('documents', [])
    
    def scan_directory(self, directory: str) -> Dict[str, List[str]]:
        """Scan directory and categorize files by type."""
        categorized_files = {}
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                category = self.get_file_category(str(file_path))
                
                if category not in categorized_files:
                    categorized_files[category] = []
                
                categorized_files[category].append(str(file_path))
        
        return categorized_files
