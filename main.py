import os
import json
import shutil
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
import re
from datetime import datetime
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box
import pyfiglet
from halo import Halo
import subprocess, time, shutil


def banner(text: str) -> None:
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    console = Console()
    panel = Panel(
        f"[bold magenta]{ascii_art}[/bold magenta]",
        title="[cyan]Local FE Agent[/cyan]",
        border_style="bold blue",
        box=box.DOUBLE,
        padding=(1, 4),
    )
    console.print(panel)

banner("LFEA")

class LFEA:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "gemma3n:e2b"     
        self.categories = {
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
    
    def query_LLM(self, prompt: str) -> str:
        """Send a query to Ollama API"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

    def searchFilesByContent(self, directory: str, query: str) -> List[Tuple[str, str]]:
        """Search files in a directory by content"""
        results = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            prompt = f"""
Does the following file content contain information related to: "{query}"?

File: {file_path.name}
Content preview:
{content[:1000]}

Answer with only "YES" or "NO", followed by a brief explanation if YES:
"""
                            ai_response = self.query_LLM(prompt)
                            
                            if ai_response.upper().startswith("YES"):
                                results.append({
                                    "file": str(file_path),
                                    "relevance": ai_response,
                                    "size": file_path.stat().st_size,
                                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                                })
                            elif ai_response.upper().startswith("NO"):
                                continue
                                
                except (UnicodeDecodeError, FileNotFoundError):
                    continue
        if results:
            return results
        else:
            return [{"message": "No relevant files found."}]

test = LFEA()
# print(test.query_ollama("Hello, how are you?"))
print(test.searchFilesByContent("D:/Personal Projects/LocalFEAgent/tests", "mango"))
