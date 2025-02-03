# Understanding Embeddings and Vector Stores

This project demonstrates the practical usage of embeddings and vector stores in AI applications. It includes examples of how to generate embeddings, store them, and perform similarity searches.

## What are Embeddings?

Embeddings are numerical representations of data (text, images, etc.) in a high-dimensional space. They capture semantic meaning and relationships between items in a way that makes them useful for:
- Similarity searches
- Recommendations
- Classification
- Information retrieval

For example, the sentences "I love programming" and "I enjoy coding" would have similar embedding vectors because they express similar meanings.

## Vector Stores

Vector stores are specialized databases designed to store and efficiently search through embedding vectors. They enable:
- Fast similarity searches
- Nearest neighbor queries
- Semantic search capabilities

## Project Structure

```
embeddings-demo/
├── README.md
├── requirements.txt
├── src/
│   ├── text_embeddings.py     # Basic text embedding generation
│   ├── vector_store.py        # Vector store operations
│   └── similarity_search.py    # Similarity search examples
└── data/
    └── sample_texts.txt       # Sample data for demonstrations
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the examples:
```bash
python src/text_embeddings.py  # Generate embeddings
python src/vector_store.py     # Store and retrieve vectors
python src/similarity_search.py # Perform similarity searches
```

3. View the visualizations:
```bash
# Navigate to the src directory
cd src

# Start a simple HTTP server
python -m http.server 8000

# Open in your browser:
# http://localhost:8000/embeddings_visualization.html
# http://localhost:8000/similarity_heatmap.html
```

## Key Concepts Demonstrated

1. **Embedding Generation**
   - Using modern embedding models
   - Processing different types of text
   - Understanding embedding dimensions

2. **Vector Store Operations**
   - Storing embeddings efficiently
   - Indexing for fast retrieval
   - Basic CRUD operations

3. **Similarity Search**
   - Cosine similarity
   - Nearest neighbor search
   - Semantic search examples

## Use Cases

1. **Semantic Search**
   - Find documents with similar meaning
   - Language-agnostic search capabilities

2. **Content Recommendations**
   - Suggest similar articles/products
   - Find related content

3. **Duplicate Detection**
   - Identify similar or duplicate content
   - Find near-duplicate texts

## Best Practices

1. **Embedding Generation**
   - Choose appropriate embedding dimensions
   - Normalize vectors when necessary
   - Consider the specific domain/use case

2. **Vector Store Usage**
   - Index vectors for faster retrieval
   - Use appropriate similarity metrics
   - Consider scalability requirements

3. **Performance Optimization**
   - Batch processing for large datasets
   - Proper indexing strategies
   - Caching frequently accessed vectors