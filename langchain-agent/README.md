# Simple Langchain Agent

This is a minimal example of a Langchain agent that demonstrates basic functionality using a single file implementation.

## Features

- Uses OpenAI's GPT model
- Implements two basic tools:
  - Web search (using DuckDuckGo)
  - Calculator
- Demonstrates agent's ability to choose appropriate tools based on the question

## Requirements

```bash
pip install langchain langchain-community langchain-core openai duckduckgo-search
```

## Usage

1. Set your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

2. Run the script:
```bash
python simple_agent.py
```

The script includes three example queries that demonstrate:
- Using the search tool
- Using the calculator tool
- Combining multiple tools to solve a problem

## Example Queries

The agent can handle queries like:
- "What is the capital of France and what's its population?"
- "What is 15% of 850?"
- "What is the population of Tokyo divided by 1000?"