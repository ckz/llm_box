import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
import uuid

# Load environment variables
load_dotenv()

class VectorDBOperations:
    def __init__(self, collection_name="demo_collection"):
        # Initialize ChromaDB client
        self.client = chromadb.Client()
        self.collection_name = collection_name
        
        # Initialize the embedding function using sentence-transformers
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='all-MiniLM-L6-v2'
        )
        
        # Get or create collection
        self.collection = self._create_collection()
    
    def _create_collection(self):
        """Create a new collection if it doesn't exist"""
        try:
            # Try to get existing collection
            collection = self.client.get_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        except:
            # Create new collection if it doesn't exist
            collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function
            )
        return collection
    
    def add_document(self, text, metadata=None):
        """Add a document to the vector database"""
        # Generate a unique ID for the document
        doc_id = str(uuid.uuid4())
        
        # Prepare metadata
        if metadata is None:
            metadata = {"text": text}
        
        # Add the document to the collection
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        return doc_id
    
    def search_similar(self, query_text, limit=5):
        """Search for similar documents"""
        # Search for similar documents
        results = self.collection.query(
            query_texts=[query_text],
            n_results=limit
        )
        
        # Format results to match the previous implementation
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'text': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'score': results['distances'][0][i] if 'distances' in results else 1.0,
                    'id': results['ids'][0][i]
                })
        
        return formatted_results
    
    def update_document(self, doc_id, new_text, new_metadata=None):
        """Update an existing document"""
        if new_metadata is None:
            new_metadata = {"text": new_text}
        
        # Update the document
        self.collection.update(
            ids=[doc_id],
            documents=[new_text],
            metadatas=[new_metadata]
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
        print(f"Score: {1 - result['score']:.4f}")  # Convert distance to similarity score
        print(f"Text: {result['text']}")
        print("---")
    
    # Update a document
    db_ops.update_document(
        doc1_id,
        "Machine learning is an application of artificial intelligence",
        {"category": "AI", "source": "demo", "updated": True}
    )
    
    # Search again to see the updated results
    print("\nUpdated search results:")
    results = db_ops.search_similar(query)
    for result in results:
        print(f"Score: {1 - result['score']:.4f}")
        print(f"Text: {result['text']}")
        print("---")

if __name__ == "__main__":
    main()