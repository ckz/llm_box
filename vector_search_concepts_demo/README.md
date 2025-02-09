# Vector Search Concepts Demo

This project demonstrates three key concepts in vector search using Langchain and FAISS:

1.  **Filtered Vector Search**: Shows how to filter vector search results based on metadata associated with the documents. This allows for more precise and targeted searches.
2.  **Self-Query Vector Search**: Illustrates how to use a language model (OpenAI LLM) to parse natural language queries and automatically apply filters to vector searches. This makes the search process more intuitive for users.
3.  **Query Expansion**: Demonstrates query expansion using an LLM to generate alternative queries to broaden the search and improve recall.

## Setup

1.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\\Scripts\\activate  # On Windows
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up OpenAI API Key:**
    Ensure you have an OpenAI API key and set it as an environment variable: `OPENAI_API_KEY=your_api_key`. You can also put this in a `.env` file in the project root directory.

## Running the Demo

Execute the `vector_search.py` script:

```bash
python vector_search_concepts_demo/vector_search.py
```

The script will:

*   Initialize a FAISS vector store with sample documents (clothing and furniture items).
*   Demonstrate each of the three vector search concepts with example queries.
*   Log the results and latency for each search type to the console.

## Concepts Explained

### 1. Filtered Vector Search

Filtered vector search allows you to combine semantic similarity search with metadata filters. This is useful when you want to narrow down search results to a specific category or based on certain attributes.

**Example:** Searching for "clothing" but only wanting results that are "blue".

### 2. Self-Query Vector Search

Self-query vector search enhances the user experience by allowing natural language queries. A language model is used to understand the query, identify filters mentioned in the query, and then perform a filtered vector search automatically.

**Example:** Asking "Show me blue clothing items". The system understands the intent to search for clothing and filter by color "blue".

### 3. Query Expansion

Query expansion aims to improve recall by broadening the search query. This is done by generating alternative queries using an LLM.

**Example:** If a user searches for "office furniture", the system generates alternative queries to ensure relevant documents are not missed.

## Performance Considerations

The script logs the latency for each type of search. In a real-world application:

*   **Latency**: Vector search latency is generally very low. Filtered searches may add a slight overhead, but are still very fast. Self-query and query expansion latency will include the time taken by the language model.
*   **Recall & Precision**:
    *   **Basic Vector Search**: Good recall for semantically similar documents, but may include irrelevant results if the query is broad.
    *   **Filtered Vector Search**: Improves precision by narrowing down results, potentially reducing recall if filters are too restrictive.
    *   **Self-Query Vector Search**: Aims to balance recall and precision by intelligently applying filters based on user intent.
    *   **Query Expansion**: Intended to improve recall, but may decrease precision if the query is expanded too broadly.

This demo provides a basic illustration of these concepts. Further experimentation and fine-tuning would be needed to optimize performance for specific use cases.