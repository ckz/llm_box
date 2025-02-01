from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains import LLMChain

def create_simple_agent(openai_api_key):
    # Initialize the language model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    
    # Initialize the search tool
    search = DuckDuckGoSearchRun()
    
    # Create a simple calculator tool using LLMChain
    calculator_prompt = PromptTemplate(
        input_variables=["question"],
        template="You are a calculator. Given the math question: {question}, provide only the numeric answer."
    )
    calculator_chain = LLMChain(llm=llm, prompt=calculator_prompt)
    
    # Define the tools
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for searching information on the internet"
        ),
        Tool(
            name="Calculator",
            func=calculator_chain.run,
            description="Useful for performing mathematical calculations"
        )
    ]
    
    # Initialize the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    return agent

def main():
    # Get OpenAI API key from environment variable
    import os
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("Please set the OPENAI_API_KEY environment variable")
        return
    
    # Create the agent
    agent = create_simple_agent(openai_api_key)
    
    # Example usage
    print("\nExample 1: Using search tool")
    response = agent.run("What is the capital of France and what's its population?")
    print(f"Response: {response}")
    
    print("\nExample 2: Using calculator tool")
    response = agent.run("What is 15% of 850?")
    print(f"Response: {response}")
    
    print("\nExample 3: Combining tools")
    response = agent.run("What is the population of Tokyo divided by 1000?")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()