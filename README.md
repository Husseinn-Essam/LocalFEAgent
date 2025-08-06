# Local File Explorer Agent (LFEA)

LLM-powered file management agent that helps you search, organize, and manage your files using natural language processing. LFEA leverages local LLM models through Ollama to provide assistance in file exploration and managment.

## Features (So far)

- **Intelligent File Search**: Search files by content symantically using natural language queries
- **Smart Organization**: Automatically categorize and organize files based on their content
- **Interactive Chat**: Converse with the AI agent about your files and get assistance
- **Local AI Processing**: Uses Ollama for privacy-focused, offline AI processing
- **Extensible Categories**: Configurable file categorization system

## Prerequisites

Before installing LFEA, ensure you have:

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
3. A gemma3n:e2b LLM model (The currently supported LLM)

### Installing Ollama

1. Visit [Ollama's website](https://ollama.ai) and download the installer for your OS
2. Install Ollama following the platform-specific instructions
3. Pull the required model:
   ```bash
   ollama pull gemma3n:e2b
   ```
4. Run Ollama server:
   ```bash
   ollama serve
   ```

## Installation

### Clone and Install Dependencies

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd LocalFEAgent
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

### Interactive Mode (Recommended)

Start the interactive chat interface:

```bash
python main.py --mode interactive
```

### Command-Line Usage

**Search for files**:
```bash
python main.py --mode search --directory "./documents" --query "meeting notes"
```

**Organize files**:
```bash
python main.py --mode organize --directory "./downloads"
```

## Usage Examples

### Interactive Mode Commands

Once in interactive mode, you can use these commands:

- `search` - Search for files by content
- `organize` - Organize files by content into folders
- `chat` - Have a conversation with the AI
- `help` - Show available commands
- `quit` - Exit the application

### Example Interactions

```
🤖 Agent: Hi! How can I help you today?

You: search for python tutorials
🤖 Agent: I'll help you search for Python tutorials.
📁 Enter directory to search (default: ./tests): ./documents
🔍 Searching for 'python tutorials' in ./documents...

You: organize my downloads folder
📁 Enter directory to organize (default: ./tests): ./downloads
🗂️ Organizing files in ./downloads...

You: what can you do?
🤖 Agent: I can help you search for files by content, organize files into categories, and have conversations about file management tasks.
```

## Configuration

### Default Configuration

LFEA comes with sensible defaults, but you can customize it by editing `src/config/default_config.json`:

```json
{
  "ollama_url": "http://localhost:11434",
  "model_name": "gemma3n:e2b",
  "capabilities": ["search", "organize", "summarize", "chat"],
  "file_categories": {
    "documents": [".pdf", ".doc", ".docx", ".txt"],
    "images": [".jpg", ".png", ".gif"],
    "code": [".py", ".js", ".html", ".css"]
  }
}
```

### Custom Configuration

Create a custom config file and use it:

```bash
python main.py --config /path/to/your/config.json
```

## Supported File Types

LFEA currently analyzes these document types:
- **Text Documents**: `.txt`, `.rtf`
- **Microsoft Office**: `.doc`, `.docx`, `.pdf`
- **OpenDocument**: `.odt`
- **Apple Pages**: `.pages`

File organization supports additional categories:
- Images, Videos, Audio files
- Spreadsheets and Presentations
- Code files and Archives
- Executables

## Command-Line Options

```bash
python main.py [OPTIONS]

Options:
  --mode {interactive,organize,search}  Operation mode (default: interactive)
  --directory, -d TEXT                  Directory to operate on (default: ./tests)
  --query, -q TEXT                      Search query (required for search mode)
  --config, -c TEXT                     Custom config file path
  --help                                Show help message
```

## Troubleshooting

### Common Issues

1. **"Error connecting to Ollama"**
   - Ensure Ollama is running: `ollama list`
   - Check if the service is on the correct port (11434)

2. **"Model not found"**
   - Pull the required model: `ollama pull gemma3n:e2b`
   - Or change the model in configuration

3. **"Permission denied" errors**
   - Ensure you have read/write permissions for target directories
   - Run with appropriate privileges if needed

4. **Unicode decode errors**
   - Some files may have encoding issues
   - LFEA will skip problematic files and continue processing

### Performance Tips

- For large directories, consider running organization in smaller batches
- The AI analysis is more accurate with text-heavy documents
- Binary files are automatically skipped during content analysis

## Project Structure

```
LocalFEAgent/
├── src/
│   ├── agent.py              # Main agent class
│   ├── core/                 # Core functionality
│   │   ├── content_analyzer.py
│   │   ├── file_manager.py
│   │   └── intent_detector.py
│   ├── llm/                  # LLM integration
│   │   └── ollama_client.py
│   ├── ui/                   # User interfaces
│   │   └── cli.py
│   └── config/               # Configuration management
│       ├── settings.py
│       └── default_config.json
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
└── README.md                # This file
```