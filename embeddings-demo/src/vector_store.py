import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class VectorStore:
    def __init__(self, dimension=384):  # default dimension for 'all-MiniLM-L6-v2'
        """Initialize FAISS index with specified dimensions."""
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
        self.texts = []  # Store original texts
        
    def add_texts(self, texts, embeddings=None):
        """Add texts and their embeddings to the store."""
        if embeddings is None:
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embeddings = model.encode(texts)
            
        # Convert to float32 (required by FAISS)
        embeddings = embeddings.astype(np.float32)
        
        # Add to FAISS index
        self.index.add(embeddings)
        # Store original texts
        self.texts.extend(texts)
        
        return len(self.texts) - len(texts), len(self.texts) - 1
    
    def similarity_search(self, query_text, k=3):
        """Search for k most similar texts."""
        # Generate embedding for query
        model = SentenceTransformer('all-MiniLM-L6-v2')
        query_embedding = model.encode([query_text])[0].astype(np.float32)
        
        # Reshape for FAISS
        query_embedding = np.array([query_embedding])
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Return results with distances
        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.texts):  # Ensure valid index
                results.append({
                    'text': self.texts[idx],
                    'distance': dist,
                    'rank': i + 1
                })
        
        return results

def main():
    # Initialize vector store
    store = VectorStore()
    
    # Get the absolute path to the sample texts
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'sample_texts.txt')
    
    # Read sample texts
    with open(data_path, 'r') as f:
        texts = f.read().splitlines()
    
    # Add texts to store
    print("Adding texts to vector store...")
    start_idx, end_idx = store.add_texts(texts)
    print(f"Added {end_idx - start_idx + 1} texts to store")
    
    # Perform sample searches
    example_queries = [
        "What is artificial intelligence?",
        "How does machine learning work?",
        "Tell me about neural networks"
    ]
    
    print("\nPerforming sample searches:")
    for query in example_queries:
        print(f"\nQuery: {query}")
        results = store.similarity_search(query)
        print("\nTop 3 most similar texts:")
        for result in results:
            print(f"{result['rank']}. {result['text']} (distance: {result['distance']:.4f})")

if __name__ == "__main__":
    main()