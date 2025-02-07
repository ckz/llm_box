from vector_ops import VectorDBOperations
import json

class KnowledgeAgent:
    def __init__(self):
        self.vector_db = VectorDBOperations(collection_name="knowledge_base")
        self.knowledge_index = {}  # Keep track of document IDs
    
    def learn(self, knowledge, category=None):
        """Learn new information by adding it to the vector database"""
        metadata = {
            "category": category if category else "general",
            "type": "knowledge"
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
                "text": result.payload["text"],
                "category": result.payload["category"],
                "relevance": result.score
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
            "updated": True
        }
        
        self.vector_db.update_document(doc_id, new_knowledge, metadata)
        self.knowledge_index[doc_id]["text"] = new_knowledge
        if category:
            self.knowledge_index[doc_id]["category"] = category

def main():
    # Create an instance of the knowledge agent
    agent = KnowledgeAgent()
    
    # Add some initial knowledge
    print("Adding initial knowledge...")
    knowledge_entries = [
        ("Python is a high-level programming language known for its simplicity.", "programming"),
        ("Vector databases are optimized for storing and searching vector embeddings.", "databases"),
        ("Machine learning models can learn patterns from data.", "ai"),
    ]
    
    for knowledge, category in knowledge_entries:
        doc_id = agent.learn(knowledge, category)
        print(f"Added knowledge in category '{category}' with ID: {doc_id}")
    
    # Test knowledge recall
    print("\nTesting knowledge recall...")
    query = "How do vector databases work?"
    results = agent.recall(query)
    
    print(f"\nResults for query: '{query}'")
    for result in results:
        print(f"\nRelevance: {result['relevance']:.4f}")
        print(f"Category: {result['category']}")
        print(f"Knowledge: {result['text']}")
    
    # Update some knowledge
    print("\nUpdating knowledge...")
    doc_id = list(agent.knowledge_index.keys())[0]  # Get first document ID
    agent.update_knowledge(
        doc_id,
        "Python is a versatile, high-level programming language known for its readability and extensive library ecosystem.",
        "programming"
    )
    
    # Verify the update
    print("\nVerifying update...")
    query = "Tell me about Python programming"
    results = agent.recall(query)
    
    print(f"\nResults for query: '{query}'")
    for result in results:
        print(f"\nRelevance: {result['relevance']:.4f}")
        print(f"Category: {result['category']}")
        print(f"Knowledge: {result['text']}")

if __name__ == "__main__":
    main()