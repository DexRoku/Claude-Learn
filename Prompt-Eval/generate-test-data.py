import json
import sys
sys.path.append('..')
from chat_client import AnthropicChat


def main():
    # Create chat instance
    prompt = """
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
    that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
    each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {
            "task": "Description of task",
        },
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """
    chat = AnthropicChat()

    chat.add_user_message(prompt)
    chat.add_assistant_message("```json")

    answer = chat.send_message(
        user_input="",
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
    )
    


if __name__ == "__main__":
    main()