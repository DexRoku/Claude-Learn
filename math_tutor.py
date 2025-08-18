# math_tutor.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()
    
    # Math tutor system prompt
    math_system = """
    You are a patient and supportive math tutor. Do not directly solve problems or give final answers. 
    Instead, guide students with hints, ask guiding questions, and encourage them to try solving it themselves. 
    If they ask for help, respond with a gentle hint — never the full solution.
    """
    
    # Send math question
    response = chat.send_message(
        "How do you solve 5x + 3 = 23 for x?", 
        system=[{"type": "text", "text": math_system}],
        max_tokens=200,
        stream=True,
    )
    
    print(f"Math Tutor: {response['answer']}")
    print(f"Tokens used: {response['input_tokens']} in, {response['output_tokens']} out")
    
    # Continue conversation
    response2 = chat.send_message("I'm not sure how to isolate x")
    print(f"Math Tutor: {response2['answer']}")

if __name__ == "__main__":
    main()