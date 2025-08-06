import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class ContentAnalyzer:
    """This class analyzes the files content using LLM"""
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.document_extensions = ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages']
    
    def search_files_by_content(self, directory: str, query: str) -> List[Dict[str, Any]]:
        """Search files by content using the LLM analysis."""
        results = []
        print(f"\n🔍 Searching for '{query}' in directory: {directory}")
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                file_extension = file_path.suffix.lower()
                
                if file_extension not in self.document_extensions:
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
                    ai_response = self.llm_client.query(prompt, 1024, 5)
                    
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
        return results if results else [{"message": "No relevant files found."}]
    
    def organize_files_by_content(self, directory: str) -> Dict[str, Any]:
        """Organize files by content into categories based on the LLM analysis."""
        print(f"🗂️ Organizing files in directory: {directory}")
        organized_files = {"moved": [], "errors": []}
        current_categories = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = Path(root) / file
                file_extension = file_path.suffix.lower()
                
                if file_extension not in self.document_extensions:
                    print(f"  ⏭️  Skipping non-document file: {file_path}")
                    continue
                
                print(f"📄 Analyzing file: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    prompt = f"ONLY REPLY WITH ONE WORD THE CATEGORY! Categorize the following content: {content[:1000]}"
                    if current_categories:
                        prompt += f"\n\nChoose one of these existing categories: {', '.join(current_categories)} only if applicable, otherwise create a new category."
                    
                    category = self.llm_client.query(prompt, 1024, 5).strip()
                    print(f"  📂 Detected category: {category}")
                    
                    if category not in current_categories:
                        current_categories.append(category)
                    
                    category_folder = Path(directory) / category
                    category_folder.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        shutil.move(str(file_path), str(category_folder / file))
                        print(f"  ✅ Moved {file} to {category_folder}")
                        organized_files["moved"].append({
                            "file": file,
                            "category": category,
                            "original_path": str(file_path),
                            "new_path": str(category_folder / file)
                        })
                    except Exception as move_error:
                        error_msg = f"Failed to move {file}: {move_error}"
                        print(f"  ❌ {error_msg}")
                        organized_files["errors"].append(error_msg)
                
                except Exception as e:
                    error_msg = f"Could not process file {file_path}: {e}"
                    print(f"  ⚠️  {error_msg}")
                    organized_files["errors"].append(error_msg)
                    continue
        
        return organized_files
