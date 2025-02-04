# Agent-based Code Generation and Review

This project demonstrates two different implementations of an AI-powered code generation and review system:

1. AutoGen Implementation (`autogen.py`)
   - Uses Microsoft's AutoGen framework
   - Implements a round-robin group chat between agents
   - Supports OpenRouter API integration
   - Includes detailed token usage tracking

2. LangChain Implementation (`langchain_version.py`)
   - Uses LangChain framework
   - Implements a simpler sequential workflow
   - Uses standard OpenAI integration
   - Focused on core functionality

Both implementations feature:
- A programmer agent that generates Python code
- A code reviewer agent that evaluates the code
- Support for complex coding tasks with requirements

## Setup

1. Install dependencies:
   ```bash
   # For AutoGen version
   pip install -r requirements.txt

   # For LangChain version
   pip install -r requirements_langchain.txt
   ```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - For AutoGen version: Add your OpenRouter API key
   - For LangChain version: Add your OpenAI API key

## Usage

### AutoGen Version
```bash
python autogen.py
```
This will:
- Create a team of agents (programmer and reviewer)
- Generate code based on the given task
- Perform code review
- Show detailed token usage statistics

### LangChain Version
```bash
python langchain_version.py
```
This will:
- Create programmer and reviewer agents
- Generate code based on the task
- Perform code review
- Display the implementation and review results

## Example Task

Both versions come with an example task to implement a FileProcessor class with requirements:
1. Support reading, writing, and appending text files
2. Include basic file statistics (line count, character count, word count)
3. Support file encryption/decryption
4. Implement error handling
5. Write complete unit tests

## Key Differences

1. AutoGen Version:
   - More complex team-based interaction
   - Round-robin chat implementation
   - Detailed token tracking
   - OpenRouter API integration

2. LangChain Version:
   - Simpler sequential workflow
   - Direct agent communication
   - Focused on core functionality
   - Standard OpenAI integration

## Requirements

- Python 3.8+
- See `requirements.txt` and `requirements_langchain.txt` for specific package versions