from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_agents():
    """Create programmer and reviewer agents using LangChain"""
    
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create programmer prompt template
    programmer_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a professional Python developer. "
            "Write clear, maintainable Python code that follows PEP8 standards. "
            "Your code should include:\n"
            "- Clear comments and docstrings\n"
            "- Proper error handling\n"
            "- Code optimization\n"
            "- Unit tests"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    # Create programmer agent
    programmer_memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    programmer = initialize_agent(
        tools=[],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=programmer_memory,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "prompt": programmer_prompt
        }
    )

    # Create reviewer prompt template
    reviewer_prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a senior code reviewer. "
            "Review code for:\n"
            "- Code standards and readability\n"
            "- Design patterns\n"
            "- Performance and efficiency\n"
            "- Security considerations\n"
            "- Test coverage\n"
            "- Potential issues\n"
            "When the code meets requirements, respond with 'Approved'."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    # Create code reviewer agent
    reviewer_memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    
    reviewer = initialize_agent(
        tools=[],
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=reviewer_memory,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "prompt": reviewer_prompt
        }
    )

    return programmer, reviewer

def run_code_review_process(task):
    """Run the code review process with programmer and reviewer agents"""
    
    programmer, reviewer = create_agents()
    
    # Step 1: Programmer creates the code
    print("\n=== Programmer's Implementation ===")
    code_implementation = programmer.run(task)
    print(code_implementation)
    
    # Step 2: Reviewer reviews the code
    print("\n=== Code Review Feedback ===")
    review_feedback = reviewer.run(f"Review this code:\n{code_implementation}")
    print(review_feedback)
    
    return {
        "implementation": code_implementation,
        "review": review_feedback
    }

if __name__ == "__main__":
    # Example task
    task = """
    Please implement a FileProcessor class with these requirements:
    1. Support reading, writing, and appending text files
    2. Include basic file statistics (line count, character count, word count)
    3. Support file encryption/decryption
    4. Implement error handling
    5. Write complete unit tests
    """
    
    result = run_code_review_process(task)