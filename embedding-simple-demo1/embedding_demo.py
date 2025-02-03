import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn as nn

# 1. Basic Text Embeddings
def basic_embeddings():
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Sample texts
    texts = [
        "I love machine learning",
        "Deep learning is fascinating",
        "The weather is nice today",
        "It's a beautiful sunny day",
        "Neural networks are powerful"
    ]
    
    # Generate embeddings
    embeddings = model.encode(texts)
    print(f"Shape of embeddings: {embeddings.shape}")
    return embeddings, texts

# 2. Custom Embedding Layer Example
class SimpleEmbedding(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super(SimpleEmbedding, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
    def forward(self, x):
        return self.embedding(x)

def demonstrate_custom_embedding():
    # Parameters
    vocab_size = 1000
    embedding_dim = 64
    
    # Create model
    model = SimpleEmbedding(vocab_size, embedding_dim)
    
    # Sample input (batch of 3 sequences, each with 4 tokens)
    sample_input = torch.LongTensor([[1, 2, 3, 4], 
                                   [5, 6, 7, 8], 
                                   [9, 10, 11, 12]])
    
    # Get embeddings
    embeddings = model(sample_input)
    print(f"Custom embedding shape: {embeddings.shape}")
    return embeddings

# 3. Vector Similarity Search
def vector_similarity_search(embeddings, texts, query_text, top_k=2):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Convert query to embedding
    query_embedding = model.encode([query_text])
    
    # Initialize FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    # Add embeddings to index
    index.add(embeddings.astype('float32'))
    
    # Search
    distances, indices = index.search(query_embedding.astype('float32'), top_k)
    
    # Return results
    results = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        results.append({
            'text': texts[idx],
            'distance': dist,
            'index': idx
        })
    
    return results

# 4. Cosine Similarity Matrix
def compute_similarity_matrix(embeddings):
    # Compute cosine similarity between all pairs
    similarity_matrix = cosine_similarity(embeddings)
    return similarity_matrix

# 5. Embedding Visualization (using dimensionality reduction)
def visualize_embeddings(embeddings, texts):
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    
    # Reduce dimensionality to 2D
    # Use lower perplexity value for small sample size
    tsne = TSNE(n_components=2, random_state=42, perplexity=2)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
    
    # Add labels
    for i, text in enumerate(texts):
        plt.annotate(text, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
    
    plt.title("2D Visualization of Text Embeddings")
    plt.xlabel("First Component")
    plt.ylabel("Second Component")
    plt.tight_layout()
    return plt

# Example usage
def main():
    # 1. Generate basic embeddings
    embeddings, texts = basic_embeddings()
    print("\n1. Basic Embeddings Generated")
    
    # 2. Demonstrate custom embedding layer
    custom_emb = demonstrate_custom_embedding()
    print("\n2. Custom Embedding Layer Demonstrated")
    
    # 3. Perform similarity search
    query = "I enjoy studying artificial intelligence"
    results = vector_similarity_search(embeddings, texts, query)
    print("\n3. Similarity Search Results:")
    for r in results:
        print(f"Text: {r['text']}, Distance: {r['distance']:.4f}")
    
    # 4. Compute similarity matrix
    similarity_matrix = compute_similarity_matrix(embeddings)
    print("\n4. Similarity Matrix Shape:", similarity_matrix.shape)
    
    # 5. Visualize embeddings
    plt = visualize_embeddings(embeddings, texts)
    print("\n5. Embedding Visualization Created")
    
    return embeddings, texts, similarity_matrix, plt

# Run the example
if __name__ == "__main__":
    embeddings, texts, similarity_matrix, plt = main()
