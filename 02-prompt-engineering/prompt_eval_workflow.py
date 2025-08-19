import json
import sys
sys.path.append('..')
from chat_client import AnthropicChat


def run_prompt(test_case):
    prompt=f""" 
    Please solve the following task:
    {test_case["task"]}
"""
    chat = AnthropicChat()
    chat.add_user_message(prompt)
    answer = chat.send_message(
        user_input="",
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
    )

    return answer

def run_test_case(test_case):
    output = run_prompt(test_case)

    score = 10
    return {"output": output, "score": score, "test_case": test_case}


def run_eval(test_case):
    results = []
    for test_case in test_case:
        result = run_test_case(test_case)
        results.append(result)
    return results


if __name__ == "__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
    results = run_eval(dataset)
    print(json.dumps(results, indent=2))  