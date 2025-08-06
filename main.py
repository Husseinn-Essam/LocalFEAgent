#!/usr/bin/env python3
"""
Local File Explorer Agent (LFEA)
Main entry point for the AI-powered file management agent.
"""

import argparse
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agent import LFEAgent
from src.ui.cli import CLI
from src.utils.banner import display_banner

def main():
    """Main entry point for the application."""
    display_banner("LFEA")
    
    parser = argparse.ArgumentParser(description="Local File Explorer Agent")
    parser.add_argument("--mode", choices=["interactive", "organize", "search"], 
                       default="interactive", help="Operation mode")
    parser.add_argument("--directory", "-d", type=str, default="./tests", 
                       help="Directory to operate on")
    parser.add_argument("--query", "-q", type=str, help="Search query")
    parser.add_argument("--config", "-c", type=str, help="Config file path")
    
    args = parser.parse_args()
    
    # Initialize the agent
    agent = LFEAgent(config_path=args.config)
    cli = CLI(agent)
    
    if args.mode == "interactive":
        cli.run_interactive()
    elif args.mode == "organize":
        agent.organize_files_by_content(args.directory)
    elif args.mode == "search":
        if not args.query:
            print("❌ Search mode requires a query. Use --query or -q")
            sys.exit(1)
        results = agent.search_files_by_content(args.directory, args.query)
        cli.display_search_results(results)

if __name__ == "__main__":
    main()