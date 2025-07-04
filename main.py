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

# from rich.console import Console
# from rich.panel import Panel
# from rich.progress import Progress, SpinnerColumn, TextColumn
# from rich import box
# import pyfiglet
# from halo import Halo
# import subprocess, time, shutil


# def banner(text: str) -> None:
#     ascii_art = pyfiglet.figlet_format(text, font="slant")
#     console = Console()
#     panel = Panel(
#         f"[bold magenta]{ascii_art}[/bold magenta]",
#         title="[cyan]Local FE Agent[/cyan]",
#         border_style="bold blue",
#         box=box.DOUBLE,
#         padding=(1, 4),
#     )
#     console.print(panel)

# banner("LFEA")

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
        "stream": False,
        "options": {
            "num_ctx": 1024,
            "num_predict": 5,
            # optional—but handy if you want the GPU filled:
            # "num_gpu": 9999
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
   
    def query_Kobold(self, prompt: str) -> str:
        """Send a query to Kobold API"""
        try:
            url = "http://localhost:5001/api/v1/generate"
            payload = {
                "prompt": prompt,
                "max_length": 5,
                "temperature": 0.7,
                "top_p": 0.9
            }
            response = requests.post(url, json=payload, timeout=120).json()
            print(response["results"][0]["text"])
            return response["results"][0]["text"].strip()
        except Exception as e:
            return f"Error connecting to Kobold: {str(e)}"
        
   
    def searchFilesByContent(self, directory: str, query: str) -> List[Tuple[str, str]]:
        """Search files in a directory by content"""
        results = []
        print(f"\n🔍 Searching for '{query}' in directory: {directory}")
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                file_extension = os.path.splitext(file)[1].lower()
                if not file_extension in self.categories['documents']:
                    print(f"  ⏭️  Skipping non-document file: {file_path}")
                    continue
                print(f"📄 Analyzing file: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                     
                        prompt = f"""
Does the following file content contain information related to: "{query}"?

File: {file_path.name}
Content preview:
{content[:1000]}

Answer with only "YES" or "NO" ONLY, without any additional text.:
"""
                        ai_response = self.query_LLM(prompt)
                        
                        if ai_response.upper().startswith("YES"):
                            print(f"  ✅ AI confirmed relevance: {file_path}")
                            results.append({
                                "file": str(file_path),
                                "relevance": ai_response,
                                "size": file_path.stat().st_size,
                                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                            })
                        elif ai_response.upper().startswith("NO"):
                            print(f"  ❌ AI rejected relevance: {file_path}")
                            continue
                    
                                
                except (UnicodeDecodeError, FileNotFoundError):
                    print(f"  ⚠️  Could not read file: {file_path}")
                    continue
        
        print(f"\n📊 Search complete. Found {len(results)} relevant files.")
        if results:
            return results
        else:
            return [{"message": "No relevant files found."}]

    def organizeFilesByContent(self,directory:str):
        """this will create folders based on file content and move files into them"""
        print(f"Organizing files in directory: {directory}")
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                file_extension = os.path.splitext(file)[1].lower()
                if not file_extension in self.categories['documents']:
                    print(f"  ⏭️  Skipping non-document file: {file_path}")
                    continue
                
                currCategories= []
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        prompt = f"ONLY REPLY WITH ONE WORD THE CATEGORY! Categorize the following content: {content[:1000]}"
                        if len(currCategories) > 0:
                            prompt += f"\n\n Choose one of the current categories: {', '.join(currCategories)} only if applicable, otherwise create a new category."
                        category = self.query_LLM(prompt)
                        print(f"  📂 Detected category for {file}: {category}")
                    category_folder = Path(directory) / category.strip()
                    category_folder.mkdir(parents=True, exist_ok=True)
                    
                    shutil.move(str(file_path), str(category_folder / file))
                    print(f"  📂 Moved {file} to {category_folder}")
                        
                except (UnicodeDecodeError, FileNotFoundError):
                    print(f"  ⚠️  Could not read file: {file_path}")
                    continue



test = LFEA()
# print(test.query_ollama("Hello, how are you?"))
print(test.organizeFilesByContent("D:/Personal Projects/LocalFEAgent/tests"))

# test.query_Kobold("Hello, how are you?")