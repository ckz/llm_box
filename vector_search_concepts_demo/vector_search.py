import os
from typing import List, Dict
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import time
from dotenv import load_dotenv
import __main__
__main__.__file__ = 'vector_search.py'

# Load environment variables
load_dotenv()

# Sample data - clothing and furniture items
sample_data = [
    Document(
        page_content="Blue cotton t-shirt with round neck",
        metadata={"type": "clothing", "color": "blue", "material": "cotton"}
    ),
    Document(
        page_content="Red leather jacket with zipper",
        metadata={"type": "clothing", "color": "red", "material": "leather"}
    ),
    Document(
        page_content="Brown wooden dining table",
        metadata={"type": "furniture", "color": "brown", "material": "wood"}
    ),
    Document(
        page_content="Black leather office chair",
        metadata={"type": "furniture", "color": "black", "material": "leather"}
    ),
    Document(
        page_content="Blue denim jeans",
        metadata={"type": "clothing", "color": "blue", "material": "denim"}
    ),
]

class VectorSearchDemo:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db = Chroma.from_documents(
            documents=sample_data,
            embedding=self.embeddings
        )
        self.llm = OpenAI(temperature=0)

    def filtered_vector_search(self, query: str, filter_dict: Dict) -> List[Document]:
        """Perform filtered vector search"""
        start_time = time.time()
        results = self.db.similarity_search(
            query,
            filter=filter_dict,
            k=2
        )
        end_time = time.time()
        print(f"\nFiltered Vector Search Latency: {end_time - start_time:.4f} seconds")
        return results

    def self_query_vector_search(self, query: str) -> List[Document]:
        """Perform self-query vector search using LLM to parse filters"""
        # Template to extract filters from natural language
        template = """
        Extract search filters from this query. Output as a Python dict with keys 'type', 'color', or 'material'.
        Only include filters explicitly mentioned. If no filters mentioned, return empty dict.
        
        Query: {query}
        
        Output format example: {{"type": "clothing", "color": "blue"}}
        """
        
        prompt = PromptTemplate(template=template, input_variables=["query"])
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        start_time = time.time()
        # Get filters from LLM
        filter_dict = eval(chain.run(query))
        
        # Perform filtered search
        results = self.db.similarity_search(
            query,
            filter=filter_dict,
            k=2
        )
        end_time = time.time()
        print(f"\nSelf-Query Vector Search Latency: {end_time - start_time:.4f} seconds")
        return results

    def query_expansion_search(self, query: str) -> List[Document]:
        """Perform query expansion search"""
        # Template for query expansion
        template = """
        Generate two alternative ways to express this search query. 
        Keep it concise and semantically similar.
        Format: original query | alternative 1 | alternative 2
        
        Query: {query}
        """
        
        prompt = PromptTemplate(template=template, input_variables=["query"])
        chain = LLMChain(llm=self.llm, prompt=prompt)
        
        start_time = time.time()
        # Get expanded queries
        expanded = chain.run(query).split("|")
        expanded = [q.strip() for q in expanded]
        
        # Combine results from all queries
        all_results = []
        for q in expanded:
            results = self.db.similarity_search(q, k=2)
            all_results.extend(results)
            
        # Remove duplicates based on content
        seen = set()
        unique_results = []
        for doc in all_results:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_results.append(doc)
                
        end_time = time.time()
        print(f"\nQuery Expansion Search Latency: {end_time - start_time:.4f} seconds")
        return unique_results[:2]  # Return top 2 results

def main():
    demo = VectorSearchDemo()
    
    # Test filtered vector search
    print("\n=== Filtered Vector Search ===")
    print("Query: 'clothing' with filter {'color': 'blue'}")
    results = demo.filtered_vector_search("clothing", {"color": "blue"})
    for doc in results:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")
    
    # Test self-query vector search
    print("\n=== Self-Query Vector Search ===")
    print("Query: 'Show me blue clothing items'")
    results = demo.self_query_vector_search("Show me blue clothing items")
    for doc in results:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")
    
    # Test query expansion search
    print("\n=== Query Expansion Search ===")
    print("Query: 'office furniture'")
    results = demo.query_expansion_search("office furniture")
    for doc in results:
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}\n")

if __name__ == "__main__":
    main()