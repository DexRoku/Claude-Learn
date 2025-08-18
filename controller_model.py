# controller_model.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()

    chat.add_user_message("Is tea or coffee better at breakfast?")
    chat.add_assistant_message("Coffee is better because it is")

    answer = chat.send_message(
        user_input="Continue your previous answer.",
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
    )

if __name__ == "__main__":
    main()