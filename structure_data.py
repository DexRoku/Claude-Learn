# controller_model.py
from chat_client import AnthropicChat

def main():
    # Create chat instance
    chat = AnthropicChat()

    chat.add_user_message("Generate a very short event bridge rule as json")
    chat.add_assistant_message("```json")

    answer = chat.send_message(
        user_input="Continue the previous answer.",
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
        stop_sequences=["```"]  # Stop when reaching the end of the code block

    )

if __name__ == "__main__":
    main()