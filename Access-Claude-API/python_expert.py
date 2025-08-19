# python_expert.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()
    
    # Python expert system prompt
    python_system = """
    You are an expert in Python programming.
    Write a Python function that checks a string for duplicate characters. I want a concise and efficient solution.
    Do not provide explanations or comments, just the code. Make sure the code is well-formatted and ready to run.
    """
    
    # Send Python question with streaming (great for code!)
    print("👤 Question: Write a Python function that checks a string for duplicate characters.")
    response = chat.send_message(
        "Write a Python function that checks a string for duplicate characters.",
        system=python_system,
        max_tokens=300,
        stream=True  # Enable streaming to see code appear line by line
    )
    
    print(f"Tokens used: streaming mode")
    print("-" * 50)
    
    # Ask for another function with streaming
    print("\n👤 Question: Now write a function to remove all duplicate characters from a string.")
    response2 = chat.send_message(
        "Now write a function to remove all duplicate characters from a string.",
        stream=True  # Watch the code being written!
    )

if __name__ == "__main__":
    main()