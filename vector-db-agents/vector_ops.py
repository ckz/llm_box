import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import numpy as np

# Load environment variables
load_dotenv()

class VectorDBOperations:
    def __init__(self, collection_name="demo_collection"):
        # Initialize Qdrant client
        self.client = QdrantClient("localhost", port=6333)
        self.collection_name = collection_name
        
        # Initialize the embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create collection if it doesn't exist
        self._create_collection()
    
    def _create_collection(self):
        """Create a new collection if it doesn't exist"""
        try:
            self.client.get_collection(self.collection_name)
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=384,  # Dimension of the model's output
                    distance=models.Distance.COSINE
                )
            )
    
    def create_embedding(self, text):
        """Create embedding for a given text"""
        return self.model.encode(text)
    
    def add_document(self, text, metadata=None):
        """Add a document to the vector database"""
        embedding = self.create_embedding(text)
        
        # Generate a random ID for the point
        point_id = np.random.randint(0, 10000000)
        
        # Prepare metadata
        if metadata is None:
            metadata = {"text": text}
        
        # Add the point to the collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=embedding.tolist(),
                    payload=metadata
                )
            ]
        )
        return point_id
    
    def search_similar(self, query_text, limit=5):
        """Search for similar documents"""
        query_vector = self.create_embedding(query_text)
        
        # Search for similar vectors
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector.tolist(),
            limit=limit
        )
        
        return search_result
    
    def update_document(self, point_id, new_text, new_metadata=None):
        """Update an existing document"""
        new_embedding = self.create_embedding(new_text)
        
        if new_metadata is None:
            new_metadata = {"text": new_text}
        
        # Update the point
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=point_id,
                    vector=new_embedding.tolist(),
                    payload=new_metadata
                )
            ]
        )

def main():
    # Example usage
    db_ops = VectorDBOperations()
    
    # Add some sample documents
    doc1_id = db_ops.add_document(
        "Machine learning is a subset of artificial intelligence",
        {"category": "AI", "source": "demo"}
    )
    
    doc2_id = db_ops.add_document(
        "Deep learning uses neural networks with multiple layers",
        {"category": "AI", "source": "demo"}
    )
    
    # Search for similar documents
    query = "What is artificial intelligence?"
    results = db_ops.search_similar(query)
    
    print(f"\nSearch results for query: '{query}'")
    for result in results:
        print(f"Score: {result.score:.4f}")
        print(f"Text: {result.payload['text']}")
        print("---")
    
    # Update a document
    db_ops.update_document(
        doc1_id,
        "Machine learning is an application of artificial intelligence",
        {"category": "AI", "source": "demo", "updated": True}
    )

if __name__ == "__main__":
    main()