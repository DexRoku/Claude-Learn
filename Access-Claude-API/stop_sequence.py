# controller_model.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()

    chat.add_user_message("Count from 1 to 10")

    answer = chat.send_message(
        user_input=None,
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
        stop_sequences=[", 5"]  # Stop when reaching 5
    )

if __name__ == "__main__":
    main()