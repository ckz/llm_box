import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.outputs import ChatResult, ChatGeneration
from typing import List, Any, Optional, Dict
from pydantic import Field, ConfigDict
import requests
import json

# Load environment variables
load_dotenv()

class OpenRouterChatModel(BaseChatModel):
    """Custom chat model for OpenRouter API."""
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    model_name: str = Field(default="anthropic/claude-2")
    temperature: float = Field(default=0.7)
    api_key: str = Field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.api_key:
            raise ValueError("OpenRouter API key is required")

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate chat response using OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "LangChain Code Review",
        }

        formatted_messages = [
            {
                "role": "system" if isinstance(msg, SystemMessage)
                else "assistant" if isinstance(msg, AIMessage)
                else "user",
                "content": msg.content
            }
            for msg in messages
        ]

        data = {
            "model": self.model_name,
            "messages": formatted_messages,
            "temperature": self.temperature,
        }
        if stop:
            data["stop"] = stop

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        result = response.json()

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=AIMessage(content=choice["message"]["content"]),
                    generation_info=dict(finish_reason=choice.get("finish_reason"))
                )
                for choice in result["choices"]
            ]
        )

    @property
    def _llm_type(self) -> str:
        return "openrouter"

class CodeReviewSystem:
    def __init__(self):
        self.llm = OpenRouterChatModel()
        
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
        code_response = self.llm.invoke(programmer_messages)
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
            review_response = self.llm.invoke(reviewer_messages)
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
            code_response = self.llm.invoke(programmer_messages)
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

if __name__ == "__main__":
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