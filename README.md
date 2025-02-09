# AI & Machine Learning Projects Collection

This repository contains a collection of projects demonstrating various aspects of AI, machine learning, and web development. Each project focuses on specific concepts and provides practical implementations.

## Project Categories

### AI Agents & LLM Integration

#### [agents_lang_auto](agents_lang_auto/)
- Demonstrates two implementations of AI-powered code generation and review systems
- Features both AutoGen (team-based) and LangChain (sequential) implementations
- Includes detailed token usage tracking and OpenRouter API integration

#### [langchain-agent](langchain-agent/)
- Simple implementation of a Langchain agent with web search and calculator tools
- Uses OpenAI's GPT model for natural language understanding
- Demonstrates tool selection based on query requirements

#### [autogen-agents](autogen-agents/)
- Financial news aggregation system using Microsoft's AutoGen framework
- Features multiple specialized agents (Planner, Google News, Yahoo Finance, Writer)
- Implements automated workflow for gathering and synthesizing financial news

#### [ai-assistant](ai-assistant/)
- Showcases best practices for integrating AI/LLM capabilities into web applications
- Features smart context management and multi-modal interactions
- Implements conversation memory patterns and knowledge base integration

### Vector Search & Embeddings

#### [embeddings-demo](embeddings-demo/)
- Comprehensive demonstration of text embeddings and vector stores
- Includes visualization tools and similarity search implementations
- Features practical examples of embedding generation and vector operations

#### [embedding-simple-demo1](embedding-simple-demo1/)
- Basic demonstration of text embeddings using Sentence Transformers
- Implements custom PyTorch embedding layers
- Includes visualization of embedding relationships using t-SNE

#### [vector_search_concepts_demo](vector_search_concepts_demo/)
- Demonstrates three key vector search concepts using Langchain and FAISS
- Features filtered vector search, self-query vector search, and query expansion
- Includes performance analysis and practical examples

#### [vector-db-agents](vector-db-agents/) & [chroma-agents](chroma-agents/)
- Implementations of knowledge agents using vector databases (Qdrant and ChromaDB)
- Demonstrates efficient knowledge storage, retrieval, and updates
- Features semantic search and metadata filtering capabilities

### Web Applications

#### [ai-quiz](ai-quiz/)
- Interactive web-based quiz application
- Tests knowledge of web development, AI, and related technologies
- Features a responsive design and real-time feedback

#### [3d-showcase](3d-showcase/)
- Demonstrates 3D graphics and animations in the browser
- Uses Three.js for 3D rendering
- Includes interactive examples and visual effects

## Getting Started

Each project has its own README with specific setup instructions. Generally, you'll need:

1. Python 3.8+ for the AI and machine learning projects
2. Node.js for some web applications
3. Various API keys (OpenAI, etc.) as specified in project READMEs
4. Required Python packages (specified in each project's requirements.txt)

## Common Requirements

Most projects require:
- OpenAI API key for LLM functionality
- Python virtual environment setup
- Basic understanding of AI/ML concepts
- Familiarity with web development (for web-based projects)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
