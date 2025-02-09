from vector_ops import VectorDBOperations
import json

class KnowledgeAgent:
    def __init__(self):
        self.vector_db = VectorDBOperations(collection_name="knowledge_base")
        self.knowledge_index = {}  # Keep track of document IDs and their metadata
    
    def learn(self, knowledge, category=None):
        """Learn new information by adding it to the vector database"""
        metadata = {
            "category": category if category else "general",
            "type": "knowledge",
            "text": knowledge  # ChromaDB requires text in metadata for filtering
        }
        
        # Add to vector database
        doc_id = self.vector_db.add_document(knowledge, metadata)
        
        # Keep track of the document ID
        self.knowledge_index[doc_id] = {
            "text": knowledge,
            "category": metadata["category"]
        }
        
        return doc_id
    
    def recall(self, query, limit=3):
        """Recall information related to the query"""
        results = self.vector_db.search_similar(query, limit=limit)
        return [
            {
                "text": result["text"],
                "category": result["metadata"]["category"],
                "relevance": 1 - result["score"]  # Convert distance to similarity score
            }
            for result in results
        ]
    
    def update_knowledge(self, doc_id, new_knowledge, category=None):
        """Update existing knowledge"""
        if doc_id not in self.knowledge_index:
            raise ValueError("Document ID not found in knowledge base")
        
        metadata = {
            "category": category if category else self.knowledge_index[doc_id]["category"],
            "type": "knowledge",
            "text": new_knowledge,
            "updated": True
        }
        
        self.vector_db.update_document(doc_id, new_knowledge, metadata)
        self.knowledge_index[doc_id]["text"] = new_knowledge
        if category:
            self.knowledge_index[doc_id]["category"] = category
    
    def get_all_by_category(self, category):
        """Get all knowledge entries in a specific category"""
        results = self.vector_db.collection.get(
            where={"category": category}
        )
        
        return [
            {
                "id": results["ids"][i],
                "text": results["documents"][i],
                "metadata": results["metadatas"][i]
            }
            for i in range(len(results["ids"]))
        ]

def main():
    # Create an instance of the knowledge agent
    agent = KnowledgeAgent()
    
    print("Adding initial knowledge...")
    # Add some initial knowledge
    knowledge_entries = [
        ("ChromaDB is an open-source embedding database for AI applications.", "databases"),
        ("Vector similarity search finds related items in high-dimensional space.", "search"),
        ("Neural networks process data through multiple layers of nodes.", "ai"),
        ("Python's simplicity makes it popular for AI development.", "programming")
    ]
    
    for knowledge, category in knowledge_entries:
        doc_id = agent.learn(knowledge, category)
        print(f"Added knowledge in category '{category}' with ID: {doc_id}")
    
    # Test knowledge recall
    print("\nTesting knowledge recall...")
    queries = [
        "How do vector databases work?",
        "Tell me about artificial intelligence",
        "What programming languages are good for AI?"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        results = agent.recall(query)
        
        for result in results:
            print(f"\nRelevance: {result['relevance']:.4f}")
            print(f"Category: {result['category']}")
            print(f"Knowledge: {result['text']}")
    
    # Test category-based retrieval
    print("\nRetrieving all entries in 'databases' category:")
    database_entries = agent.get_all_by_category("databases")
    for entry in database_entries:
        print(f"\nID: {entry['id']}")
        print(f"Text: {entry['text']}")
        print(f"Category: {entry['metadata']['category']}")
    
    # Update some knowledge
    print("\nUpdating knowledge...")
    doc_id = list(agent.knowledge_index.keys())[0]  # Get first document ID
    agent.update_knowledge(
        doc_id,
        "ChromaDB is a modern, open-source embedding database optimized for AI and machine learning applications.",
        "databases"
    )
    
    # Verify the update
    print("\nVerifying update with new query...")
    query = "Tell me about ChromaDB"
    results = agent.recall(query)
    
    print(f"\nResults for query: '{query}'")
    for result in results:
        print(f"\nRelevance: {result['relevance']:.4f}")
        print(f"Category: {result['category']}")
        print(f"Knowledge: {result['text']}")

if __name__ == "__main__":
    main()