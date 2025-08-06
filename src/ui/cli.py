from typing import List, Dict, Any

class CLI:
    """Command-line interface for the Local File Explorer Agent."""
    
    def __init__(self, agent):
        self.agent = agent
    
    def run_interactive(self):
        """Run interactive chat mode."""
        print("🤖 Agent: Hi! How can I help you today?")
        print("Available commands: search, organize, chat, help, quit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🤖 Agent: Goodbye! 👋")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                # Detect intent and handle accordingly
                intent = self.agent.detect_intent(user_input)
                
                if intent == "search":
                    self._handle_search(user_input)
                elif intent == "organize":
                    self._handle_organize()
                elif intent == "chat":
                    response = self.agent.chat(user_input)
                    print(f"🤖 Agent: {response}")
                else:
                    print("🤖 Agent: I'm not sure what you want to do. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n🤖 Agent: Goodbye! 👋")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    def _handle_search(self, query: str):
        """Handle search intent."""
        directory = input("📁 Enter directory to search (default: ./tests): ").strip() or "./tests"
        print(f"🔍 Searching for '{query}' in {directory}...")
        
        results = self.agent.search_files_by_content(directory, query)
        self.display_search_results(results)
    
    def _handle_organize(self):
        """Handle organize intent."""
        directory = input("📁 Enter directory to organize (default: ./tests): ").strip() or "./tests"
        print(f"🗂️ Organizing files in {directory}...")
        
        result = self.agent.organize_files_by_content(directory)
        self._display_organize_results(result)
    
    def display_search_results(self, results: List[Dict[str, Any]]):
        """Display search results."""
        if not results or (len(results) == 1 and "message" in results[0]):
            print("❌ No relevant files found.")
            return
        
        print(f"\n📊 Found {len(results)} relevant files:")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. 📄 {result['file']}")
            print(f"   Size: {result['size']} bytes")
            print(f"   Modified: {result['modified']}")
            print(f"   Relevance: {result['relevance']}")
            print()
    
    def _display_organize_results(self, result: Dict[str, Any]):
        """Display organization results."""
        moved_files = result.get("moved", [])
        errors = result.get("errors", [])
        
        if moved_files:
            print(f"\n✅ Successfully moved {len(moved_files)} files:")
            for file_info in moved_files:
                print(f"  📄 {file_info['file']} → 📁 {file_info['category']}")
        
        if errors:
            print(f"\n❌ Encountered {len(errors)} errors:")
            for error in errors:
                print(f"  ⚠️ {error}")
        
        if not moved_files and not errors:
            print("ℹ️ No files were organized.")
    
    def _show_help(self):
        """Show help information."""
        print("\n🆘 Available Commands:")
        print("  search   - Search for files by content")
        print("  organize - Organize files by content into folders")
        print("  chat     - Have a conversation with the AI")
        print("  help     - Show this help message")
        print("  quit     - Exit the application")
        print("\nCapabilities:", ", ".join(self.agent.get_capabilities()))
