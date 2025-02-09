# ChromaDB Agents Demo

This project demonstrates the integration of AI agents with ChromaDB for efficient knowledge storage, retrieval, and updates. It showcases how to use vector embeddings for semantic search and knowledge management using ChromaDB's simple yet powerful API.

## Project Structure

```
chroma-agents/
├── requirements.txt      # Project dependencies
├── vector_ops.py        # Core vector database operations using ChromaDB
├── knowledge_agent.py   # Knowledge management agent implementation
└── README.md           # Project documentation
```

## Prerequisites

- Python 3.8+
- Required Python packages (listed in requirements.txt)

## Setup Instructions

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the demo:
   ```bash
   python knowledge_agent.py
   ```

## Design Overview

### Vector Database Operations (`vector_ops.py`)

The `VectorDBOperations` class provides core functionality for interacting with ChromaDB:

- **Initialization**: Sets up ChromaDB client and creates a collection if it doesn't exist
- **Embedding Generation**: Uses SentenceTransformer model for text embeddings
- **CRUD Operations**:
  - Create: Add new documents with embeddings
  - Read: Search for similar documents using vector similarity
  - Update: Modify existing documents while maintaining vector relationships
  - Query: Filter documents by metadata

### Knowledge Agent (`knowledge_agent.py`)

The `KnowledgeAgent` class builds upon the vector operations to provide a higher-level interface for knowledge management:

- **Learning**: Adds new knowledge entries to ChromaDB with metadata
- **Recall**: Retrieves relevant information based on semantic similarity
- **Knowledge Updates**: Modifies existing knowledge while maintaining semantic relationships
- **Category Filtering**: Supports retrieving all entries in a specific category

### Key Features

1. **Semantic Search**: Uses vector embeddings to find semantically similar content
2. **Metadata Management**: Tracks additional information about knowledge entries
3. **Efficient Updates**: Maintains document relationships while allowing content updates
4. **Category Organization**: Supports categorization and filtering of knowledge entries
5. **Simple Integration**: ChromaDB's straightforward API makes it easy to work with

## Usage Examples

### Basic Usage

```python
from knowledge_agent import KnowledgeAgent

# Initialize agent
agent = KnowledgeAgent()

# Add new knowledge
doc_id = agent.learn(
    "ChromaDB is an open-source embedding database for AI applications.",
    category="databases"
)

# Recall information
results = agent.recall("How do vector databases work?")
for result in results:
    print(f"Relevance: {result['relevance']}")
    print(f"Knowledge: {result['text']}")

# Update knowledge
agent.update_knowledge(
    doc_id,
    "ChromaDB is a modern, open-source embedding database optimized for AI applications.",
    category="databases"
)
```

### Advanced Features

1. **Batch Learning**:
   ```python
   knowledge_entries = [
       ("Neural networks process data through layers.", "ai"),
       ("Vector similarity finds related items.", "search")
   ]
   for knowledge, category in knowledge_entries:
       agent.learn(knowledge, category)
   ```

2. **Category-based Retrieval**:
   ```python
   # Get all entries in a specific category
   database_entries = agent.get_all_by_category("databases")
   ```

3. **Filtered Recall**:
   ```python
   # Get top 3 most relevant results
   results = agent.recall("machine learning", limit=3)
   ```

## Technical Details

- **Embedding Model**: Uses the 'all-MiniLM-L6-v2' model from SentenceTransformers
- **Vector Storage**: ChromaDB for efficient similarity search and filtering
- **Persistence**: ChromaDB automatically handles persistence of embeddings and metadata
- **Filtering**: Supports metadata-based filtering using ChromaDB's where clauses

## Advantages of ChromaDB

1. **Simplicity**: Easy to set up and use with a Python-first API
2. **Built-in Persistence**: Automatic handling of data storage
3. **Metadata Filtering**: Rich querying capabilities using metadata
4. **Lightweight**: Runs in-process without external dependencies
5. **Open Source**: Active community and regular updates

## Future Enhancements

1. Implement batch processing for better performance
2. Add support for document chunking
3. Implement more advanced filtering patterns
4. Add support for multiple embedding models
5. Implement cross-collection operations
6. Add data export/import capabilities

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this code for your own projects!