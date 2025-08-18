# chat_client.py
from dotenv import load_dotenv
import os
from anthropic import Anthropic

class AnthropicChat:
    def __init__(self):
        """Initialize the chat client with API key and default settings."""
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self._check_api_key()
        
        self.client = Anthropic()
        self.model = "claude-sonnet-4-0"
        self.messages = []
    
    def _check_api_key(self):
        """Check if API key is loaded properly."""
        if self.api_key:
            print("API key loaded ✅")
        else:
            print("API key not found ❌")
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    
    def add_user_message(self, text: str):
        """Add a user message to the conversation."""
        self.messages.append({"role": "user", 
                              "content": [{"type": "text", "text": text}]})

    def add_assistant_message(self, text: str):
        """Add an assistant message to the conversation."""
        self.messages.append({"role": "assistant", "content": [{"type": "text", "text": text}]})

    def send_message(self, user_input=None, system=None, max_tokens=100, stream=False, stop_sequences=[]):
        """Send a message and get response."""
        if user_input is None:
            self.add_user_message(str(user_input))

        if stream: 
            print("Assistant: ", end="", flush=True)
            full_answer = ""

            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                messages=self.messages,
                system=system, # type: ignore
                stop_sequences=stop_sequences
            ) as stream:
                for text_chunk in stream.text_stream:
                    print(text_chunk, end="", flush=True)

            print()  # New line after streaming
            self.add_assistant_message(full_answer)
            return {
                'answer': full_answer,
                'input_tokens': 0,
                'output_tokens': 0
            }

        else:

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=self.messages,
                system=system # type: ignore
            )
            
            answer = response.content[0].text # type: ignore
            self.add_assistant_message(answer)
            
            return {
                'answer': answer,
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens
            }
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.messages = []