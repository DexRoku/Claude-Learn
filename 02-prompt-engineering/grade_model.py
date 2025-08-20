import json
import sys
import re
sys.path.append('..')
from chat_client import AnthropicChat


def run_prompt(test_case):
    prompt = f""" 
    Please solve the following task:
    {test_case["task"]}
    """
    chat = AnthropicChat()
    chat.add_user_message(prompt)
    answer = chat.send_message(
        user_input=None,
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=200,
        stream=True,
    )
    return answer


def grade_by_model(test_case, output):
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {test_case["task"]}
    Solution: {output}
    
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """
    
    chat = AnthropicChat()
    chat.add_user_message(eval_prompt)
    chat.add_assistant_message("```json")
    evaluation = chat.send_message(
        user_input=None,  # ✅ Changed from "" to None
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=500,  # Increased tokens
        stream=False,
        stop_sequences=[]  # Remove stop sequences to avoid cutting off JSON
    )
    
    try:
        # Extract the actual answer text from the response dict
        answer_text = evaluation.get('answer', '')
        
        # DEBUG: Print what you actually get
        print(f"Answer text: {answer_text}")
        
        if answer_text:
            # Try to parse JSON from the answer text
            cleaned = answer_text.strip()
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = json.loads(cleaned)
                
            # Debug: print the parsed JSON structure
            print(f"Parsed JSON keys: {list(parsed.keys())}")
            print(f"Parsed JSON: {parsed}")
            
            return {
                "score": parsed.get("score", 1),
                "reasoning": parsed.get("reasoning", "No reasoning provided"),  
                "strengths": parsed.get("strengths", parsed.get("strength", [])),  # Try both 'strengths' and 'strength'
                "weaknesses": parsed.get("weaknesses", parsed.get("weakness", []))  # Try both 'weaknesses' and 'weakness'
            }
            
    except Exception as e:
        print(f"Error processing evaluation: {e}")
        print(f"Raw evaluation: {evaluation}")
    
    # Fallback for any error
    return {
        "score": 1,
        "reasoning": "Failed to parse evaluation response",
        "strengths": [],
        "weaknesses": ["Evaluation parsing failed"]
    }


def run_test_case(test_case):
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case, output)
    
    return {
        "output": output,
        "score": model_grade["score"],
        "test_case": test_case,
        "reasoning": model_grade["reasoning"],
        "strengths": model_grade["strengths"],
        "weaknesses": model_grade["weaknesses"]
    }


def run_eval(dataset):
    results = []
    for i, test_case in enumerate(dataset):
        print(f"Running test case {i+1}/{len(dataset)}")
        result = run_test_case(test_case)
        results.append(result)

    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"Average score: {avg_score:.2f}")
    return results


if __name__ == "__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
    
    results = run_eval(dataset)
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n=== EVALUATION SUMMARY ===")
    for i, result in enumerate(results):
        print(f"Test {i+1}: Score {result['score']}/10")
        print(f"  Task: {result['test_case']['task'][:50]}...")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Strengths: {', '.join(result['strengths'])}")
        print(f"  Weaknesses: {', '.join(result['weaknesses'])}")