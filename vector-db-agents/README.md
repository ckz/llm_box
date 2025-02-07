# Vector Database Agents Demo

This project demonstrates the integration of AI agents with vector databases (Qdrant) for efficient knowledge storage, retrieval, and updates. It showcases how to use vector embeddings for semantic search and knowledge management.

## Project Structure

```
vector-db-agents/
├── requirements.txt      # Project dependencies
├── vector_ops.py        # Core vector database operations
├── knowledge_agent.py   # Knowledge management agent implementation
└── README.md           # Project documentation
```

## Prerequisites

- Python 3.8+
- Qdrant running locally (or accessible via network)
- Required Python packages (listed in requirements.txt)

## Setup Instructions

1. Install Qdrant:
   ```bash
   # Using Docker
   docker pull qdrant/qdrant
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the demo:
   ```bash
   python knowledge_agent.py
   ```

## Design Overview

### Vector Database Operations (`vector_ops.py`)

The `VectorDBOperations` class provides core functionality for interacting with the Qdrant vector database:

- **Initialization**: Sets up connection to Qdrant and creates a collection if it doesn't exist
- **Embedding Generation**: Uses SentenceTransformer model to convert text into vector embeddings
- **CRUD Operations**:
  - Create: Add new documents with embeddings
  - Read: Search for similar documents using cosine similarity
  - Update: Modify existing documents while maintaining vector relationships
  - Delete: (Not implemented but can be added as needed)

### Knowledge Agent (`knowledge_agent.py`)

The `KnowledgeAgent` class builds upon the vector operations to provide a higher-level interface for knowledge management:

- **Learning**: Adds new knowledge entries to the vector database with metadata
- **Recall**: Retrieves relevant information based on semantic similarity
- **Knowledge Updates**: Modifies existing knowledge while maintaining semantic relationships

### Key Features

1. **Semantic Search**: Uses vector embeddings to find semantically similar content rather than exact matches
2. **Metadata Management**: Tracks additional information about knowledge entries
3. **Efficient Updates**: Maintains document relationships while allowing content updates
4. **Category Organization**: Supports categorization of knowledge entries

## Usage Examples

### Basic Usage

```python
from knowledge_agent import KnowledgeAgent

# Initialize agent
agent = KnowledgeAgent()

# Add new knowledge
doc_id = agent.learn(
    "Vector databases are optimized for storing and searching vector embeddings.",
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
    "Vector databases efficiently store and search high-dimensional vectors using specialized indexing.",
    category="databases"
)
```

### Advanced Features

1. **Batch Learning**:
   ```python
   knowledge_entries = [
       ("Python is a high-level language.", "programming"),
       ("Vector search uses similarity metrics.", "databases")
   ]
   for knowledge, category in knowledge_entries:
       agent.learn(knowledge, category)
   ```

2. **Filtered Recall**:
   ```python
   # Get top 3 most relevant results
   results = agent.recall("programming languages", limit=3)
   ```

## Technical Details

- **Embedding Model**: Uses the 'all-MiniLM-L6-v2' model from SentenceTransformers
- **Vector Dimension**: 384-dimensional embeddings
- **Similarity Metric**: Cosine similarity for vector comparisons
- **Storage**: Qdrant vector database for efficient similarity search

## Future Enhancements

1. Implement deletion operations
2. Add batch processing capabilities
3. Integrate with other vector databases
4. Add support for document chunking
5. Implement vector index persistence
6. Add more sophisticated querying capabilities

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this code for your own projects!