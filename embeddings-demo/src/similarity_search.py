from sentence_transformers import SentenceTransformer
import numpy as np
from vector_store import VectorStore
import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity
import os

class SimilaritySearchDemo:
    def __init__(self):
        """Initialize the demo with necessary components."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_store = VectorStore()
        
    def load_and_index_texts(self, filepath):
        """Load texts and create vector store index."""
        with open(filepath, 'r') as f:
            texts = f.read().splitlines()
        
        # Generate embeddings
        embeddings = self.model.encode(texts)
        
        # Add to vector store
        self.vector_store.add_texts(texts, embeddings)
        return texts, embeddings
    
    def find_similar_pairs(self, embeddings, texts, threshold=0.7):
        """Find all pairs of texts with similarity above threshold."""
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find pairs above threshold
        similar_pairs = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                if similarity_matrix[i][j] > threshold:
                    similar_pairs.append({
                        'text1': texts[i],
                        'text2': texts[j],
                        'similarity': similarity_matrix[i][j]
                    })
        
        return similar_pairs
    
    def create_similarity_heatmap(self, embeddings, texts):
        """Create and save a similarity heatmap visualization."""
        similarity_matrix = cosine_similarity(embeddings)
        
        # Create DataFrame for heatmap
        df = pd.DataFrame(similarity_matrix, columns=range(len(texts)))
        
        # Create heatmap
        fig = px.imshow(
            similarity_matrix,
            labels=dict(x="Text Index", y="Text Index", color="Cosine Similarity"),
            title="Text Similarity Heatmap"
        )
        
        # Add text labels
        fig.update_traces(text=np.round(similarity_matrix, 2), texttemplate="%{text}")
        
        # Save visualization in the script's directory
        output_path = os.path.join(os.path.dirname(__file__), "similarity_heatmap.html")
        fig.write_html(output_path)
        print(f"Heatmap saved as '{output_path}'")
    
    def semantic_clustering(self, embeddings, texts, n_neighbors=3):
        """Find semantic clusters in the texts."""
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # For each text, find its most similar neighbors
        clusters = []
        for i in range(len(texts)):
            # Get indices of most similar texts (excluding self)
            similar_indices = np.argsort(similarity_matrix[i])[::-1][1:n_neighbors+1]
            
            cluster = {
                'center_text': texts[i],
                'similar_texts': [texts[j] for j in similar_indices],
                'similarities': [similarity_matrix[i][j] for j in similar_indices]
            }
            clusters.append(cluster)
        
        return clusters

def main():
    # Initialize demo
    demo = SimilaritySearchDemo()
    
    # Get the absolute path to the sample texts
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(os.path.dirname(current_dir), 'data', 'sample_texts.txt')
    
    # Load and index texts
    print("Loading and indexing texts...")
    texts, embeddings = demo.load_and_index_texts(data_path)
    
    # Find similar pairs
    print("\nFinding similar text pairs...")
    similar_pairs = demo.find_similar_pairs(embeddings, texts, threshold=0.7)
    print("\nHighly similar text pairs:")
    for pair in similar_pairs:
        print(f"\nSimilarity: {pair['similarity']:.4f}")
        print(f"Text 1: {pair['text1']}")
        print(f"Text 2: {pair['text2']}")
    
    # Create similarity heatmap
    print("\nCreating similarity heatmap...")
    demo.create_similarity_heatmap(embeddings, texts)
    
    # Perform semantic clustering
    print("\nPerforming semantic clustering...")
    clusters = demo.semantic_clustering(embeddings, texts)
    print("\nSemantic clusters:")
    for i, cluster in enumerate(clusters, 1):
        print(f"\nCluster {i} - Center: {cluster['center_text']}")
        print("Similar texts:")
        for text, sim in zip(cluster['similar_texts'], cluster['similarities']):
            print(f"- {text} (similarity: {sim:.4f})")
    
    # Demonstrate vector store search
    print("\nDemonstrating vector store search...")
    query = "How does AI learn and improve?"
    results = demo.vector_store.similarity_search(query)
    print(f"\nQuery: {query}")
    print("Most similar texts:")
    for result in results:
        print(f"{result['rank']}. {result['text']} (distance: {result['distance']:.4f})")

if __name__ == "__main__":
    main()