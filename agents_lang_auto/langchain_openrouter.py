import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from typing import List
import json

# Load environment variables
load_dotenv()

# Configure OpenRouter API
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

def create_chat_model():
    """Create a chat model using OpenRouter."""
    return ChatOpenAI(
        model="anthropic/claude-2",  # You can change this to other models available on OpenRouter
        temperature=0.7,
        headers={
            "HTTP-Referer": "http://localhost:3000",  # Required by OpenRouter
            "X-Title": "LangChain Code Review",  # Optional
        }
    )

class CodeReviewSystem:
    def __init__(self):
        self.llm = create_chat_model()
        self.memory = ConversationBufferMemory()
        
        # Define system messages for both agents
        self.programmer_system = SystemMessage(content="""You are a professional Python developer.
Please write clear, maintainable Python code that follows PEP8 standards.
Your code should include:
- Clear comments and docstrings
- Proper error handling
- Code optimization
- Unit tests""")
        
        self.reviewer_system = SystemMessage(content="""You are a senior code reviewer.
Please review the code thoroughly, considering:
- Code readability and standards compliance
- Design patterns
- Performance and efficiency
- Security considerations
- Test coverage
- Potential issues
When the code meets all requirements, respond with 'Approved'.""")

    def run_review_session(self, task: str) -> List[dict]:
        """Run a complete code review session."""
        conversation = []
        
        # Step 1: Programmer writes the code
        programmer_messages = [
            self.programmer_system,
            HumanMessage(content=task)
        ]
        code_response = self.llm(programmer_messages)
        conversation.append({
            "role": "programmer",
            "content": code_response.content
        })
        
        # Step 2: Start review process
        while True:
            reviewer_messages = [
                self.reviewer_system,
                HumanMessage(content=code_response.content)
            ]
            review_response = self.llm(reviewer_messages)
            conversation.append({
                "role": "reviewer",
                "content": review_response.content
            })
            
            # Check if code is approved
            if "Approved" in review_response.content:
                break
                
            # If not approved, let programmer revise
            programmer_messages = [
                self.programmer_system,
                HumanMessage(content=f"Please revise the code based on this review:\n{review_response.content}")
            ]
            code_response = self.llm(programmer_messages)
            conversation.append({
                "role": "programmer",
                "content": code_response.content
            })
        
        return conversation

def print_formatted_result(conversation):
    """Print the conversation in a formatted way."""
    print("\n" + "="*60)
    print("Code Review Process".center(60))
    print("="*60 + "\n")
    
    for msg in conversation:
        if msg["role"] == "programmer":
            print("👨‍💻 Developer Submission:")
        else:
            print("🔍 Code Review Feedback:")
        print("-" * 40)
        print(f"{msg['content']}\n")
    
    print("="*60)
    print("Review Complete".center(60))
    print("="*60)

def main():
    # Example task
    task = """
    Please implement a FileProcessor class with the following requirements:
    1. Support reading, writing, and appending text files
    2. Include basic file statistics (line count, character count, word count)
    3. Support file encryption/decryption
    4. Implement error handling
    5. Write complete unit tests
    """
    
    # Create and run the review system
    review_system = CodeReviewSystem()
    conversation = review_system.run_review_session(task)
    
    # Print results
    print_formatted_result(conversation)

if __name__ == "__main__":
    main()