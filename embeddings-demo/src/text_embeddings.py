from sentence_transformers import SentenceTransformer
import numpy as np
import torch
import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA
import os

class TextEmbeddingDemo:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initialize with a pre-trained sentence transformer model."""
        self.model = SentenceTransformer(model_name)
        
    def generate_embeddings(self, texts):
        """Generate embeddings for a list of texts."""
        return self.model.encode(texts)
    
    def visualize_embeddings(self, embeddings, texts, title="Text Embeddings Visualization"):
        """Visualize embeddings in 2D using PCA."""
        # Reduce dimensions to 2D for visualization
        pca = PCA(n_components=2)
        embeddings_2d = pca.fit_transform(embeddings)
        
        # Create a DataFrame for plotting
        df = pd.DataFrame(embeddings_2d, columns=['PC1', 'PC2'])
        df['text'] = texts
        
        # Create interactive scatter plot
        fig = px.scatter(
            df, x='PC1', y='PC2', 
            hover_data=['text'],
            title=title
        )
        
        # Save the plot as HTML
        fig.write_html("embeddings_visualization.html")
        print("Visualization saved as 'embeddings_visualization.html'")

def main():
    # Initialize the demo
    demo = TextEmbeddingDemo()
    
    # Read sample texts
    with open('../data/sample_texts.txt', 'r') as f:
        texts = f.read().splitlines()
    
    # Generate embeddings
    print("Generating embeddings...")
    embeddings = demo.generate_embeddings(texts)
    
    # Print embedding information
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(f"Number of dimensions: {embeddings.shape[1]}")
    
    # Example of comparing similarity between two texts
    text1_idx = 0  # "Machine learning is a subset of artificial intelligence"
    text2_idx = 1  # "AI systems can learn from experience and improve over time"
    
    similarity = np.dot(embeddings[text1_idx], embeddings[text2_idx]) / \
                (np.linalg.norm(embeddings[text1_idx]) * np.linalg.norm(embeddings[text2_idx]))
    
    print(f"\nSimilarity between first two texts: {similarity:.4f}")
    
    # Visualize embeddings
    print("\nCreating visualization...")
    demo.visualize_embeddings(embeddings, texts)
    
    print("\nDemonstration completed! Check 'embeddings_visualization.html' for the visualization.")

if __name__ == "__main__":
    main()