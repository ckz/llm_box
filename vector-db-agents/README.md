# Vector Database Agent with ChromaDB

This project demonstrates a simple knowledge agent that uses ChromaDB as its vector database for storing and retrieving information. It allows you to add documents, search for similar documents, and update existing documents.

**This README.md assumes you have modified the original `vector_ops.py` file to use ChromaDB instead of Qdrant.**

## Prerequisites

*   Python 3.7+
*   `chromadb`
*   `python-dotenv`
*   `sentence-transformers` (likely installed as a dependency of `chromadb`)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd vector-db-agents
    ```

2.  **Important:** Update the `requirements.txt` file to include `chromadb`, `python-dotenv`, and remove any Qdrant-specific dependencies. It should look something like this:

    ```
    chromadb
    python-dotenv
    ```

3.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### VectorDBOperations

The `VectorDBOperations` class provides the core functionality for interacting with the ChromaDB vector database.

```python
from vector_ops import VectorDBOperations

# Initialize the vector database operations
db_ops = VectorDBOperations(collection_name="my_collection")

# Add some documents
doc1_id = db_ops.add_document(
    "Machine learning is a subset of artificial intelligence",  # Document text
    {"category": "AI", "source": "example"}  # Metadata (optional)
)
doc2_id = db_ops.add_document(
    "ChromaDB is a vector database.",  # Document text
    {"category": "Databases", "source": "example"}  # Metadata (optional)
)

# Search for similar documents
query = "What is AI?"
results = db_ops.search_similar(query, limit=3)

print(f"Search results for: {query}")
for result in results:
    print(f"  Score: {result['score']}")
    print(f"  Text: {result['text']}")
    print(f"  Metadata: {result['metadata']}")
    print("---")

# Update a document
db_ops.update_document(
    doc1_id,  # ID of the document to update
    "Machine learning is an application of artificial intelligence.",  # New document text
    {"category": "AI", "source": "example", "updated": True}  # New metadata (optional)
)

# Search again to see updated document
results = db_ops.search_similar(query, limit=3)


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

## License

MIT License - feel free to use this code for your own projects!