# interactive_chat.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()
    
    print("🤖 Interactive Chat Started!")
    print("Type 'quit' to exit, 'clear' to clear conversation history")
    print("Type 'stream on' to enable streaming, 'stream off' to disable")
    print("-" * 60)
    
    # Optional system prompt
    system_prompt = """
    You are a helpful AI assistant. Be conversational, friendly, and concise in your responses.
    """
    
    streaming_enabled = False  # Track streaming state
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == 'clear':
            chat.clear_conversation()
            print("🧹 Conversation cleared!")
            continue
        
        if user_input.lower() == 'stream on':
            streaming_enabled = True
            print("🌊 Streaming enabled!")
            continue
            
        if user_input.lower() == 'stream off':
            streaming_enabled = False
            print("📄 Streaming disabled!")
            continue
        
        if not user_input:
            continue
        
        try:
            response = chat.send_message(
                user_input, 
                system=system_prompt,
                max_tokens=500,
                stream=streaming_enabled  # Use streaming based on user choice
            )
            
            # Only print this if NOT streaming (streaming already prints)
            if not streaming_enabled:
                print(f"🤖 Assistant: {response['answer']}")
                print(f"   (Tokens: {response['input_tokens']} in, {response['output_tokens']} out)")
            else:
                print("   (Streaming mode - token count not available)")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()