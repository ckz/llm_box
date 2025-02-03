# Text Embeddings Simple Demo

This project demonstrates the basic usage of text embeddings using the Sentence Transformers library and various techniques for text similarity analysis and visualization.

## What are Text Embeddings?

Text embeddings are numerical representations of text that capture semantic meaning. They convert words or pieces of text into high-dimensional vectors, where similar texts are positioned closer together in the vector space. This makes it possible to:
- Compare the similarity between different texts
- Find related content
- Organize text by topic
- Build semantic search systems

## Implementation Details

The demo implements the following key features:

1. **Basic Text Embeddings**
   - Uses the 'all-MiniLM-L6-v2' model from Sentence Transformers
   - Converts sample texts into vector representations
   - Demonstrates batch processing of multiple texts

2. **Custom Embedding Layer**
   - Implements a PyTorch-based custom embedding layer
   - Shows how to create embeddings from scratch
   - Demonstrates handling batched input sequences

3. **Vector Similarity Search**
   - Uses FAISS for efficient similarity search
   - Implements k-nearest neighbor search
   - Returns most similar texts with their distances

4. **Cosine Similarity Matrix**
   - Computes pairwise similarities between all text embeddings
   - Uses scikit-learn's cosine_similarity function
   - Helps visualize relationships between all texts

5. **Embedding Visualization**
   - Reduces high-dimensional embeddings to 2D using t-SNE
   - Creates scatter plots of text relationships
   - Uses optimized perplexity for small datasets
   - Adds text labels for easy interpretation

## Requirements

The project requires the following Python packages:
```
numpy>=1.24.0
sentence-transformers>=2.2.2
faiss-cpu>=1.7.4
scikit-learn>=1.3.0
torch>=2.0.0
matplotlib>=3.7.0
```

## Installation

1. Clone the repository and navigate to the project directory

2. Install the required dependencies using the requirements.txt file:
```bash
pip install -r requirements.txt
```

## Usage

Run the demo:
```bash
python embedding_demo.py
```

The script will:
- Generate embeddings for sample texts
- Demonstrate custom embedding layer functionality
- Perform similarity search with a query
- Compute a similarity matrix
- Create a visualization of the embeddings

## Code Structure

- `basic_embeddings()`: Generates embeddings for sample texts
- `SimpleEmbedding`: Custom PyTorch embedding layer class
- `demonstrate_custom_embedding()`: Shows custom embedding usage
- `vector_similarity_search()`: Implements FAISS-based similarity search
- `compute_similarity_matrix()`: Creates pairwise similarity matrix
- `visualize_embeddings()`: Creates 2D visualization of embeddings with optimized t-SNE parameters

## Example Output

The demo includes sample texts about machine learning and weather, showing how the embedding space captures semantic relationships. The visualization will show similar concepts clustered together, while unrelated topics will be farther apart. The t-SNE visualization is optimized for small datasets with appropriate perplexity settings.

## Learning Points

1. Understanding how text embeddings capture semantic meaning
2. Learning about different similarity metrics (L2 distance, cosine similarity)
3. Exploring efficient similarity search with FAISS
4. Visualizing high-dimensional data in 2D space using t-SNE with appropriate parameters
5. Implementing custom embedding layers with PyTorch