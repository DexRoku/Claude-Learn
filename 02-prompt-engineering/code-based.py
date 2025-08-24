import json
import sys
import re
import ast
sys.path.append('..')
from chat_client import AnthropicChat


def validate_json(content):
    """Validate JSON content and return score, feedback"""
    try:
        json.loads(content)
        return 10, "Valid JSON structure"
    except json.JSONDecodeError as e:
        return 0, f"Invalid JSON: {str(e)}"


def validate_python(content):
    """Validate Python code and return score, feedback"""
    try:
        # Try to parse the code
        ast.parse(content)
        return 10, "Valid Python syntax"
    except SyntaxError as e:
        return 0, f"Invalid Python syntax: {str(e)}"
    except Exception as e:
        return 0, f"Python validation error: {str(e)}"


def validate_regex(content):
    """Validate regex pattern and return score, feedback"""
    try:
        re.compile(content)
        return 10, "Valid regex pattern"
    except re.error as e:
        return 0, f"Invalid regex: {str(e)}"


def extract_content_by_type(output, content_type):
    """Extract relevant content based on type"""
    if content_type == "json":
        # Look for JSON in code blocks or standalone
        json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL | re.IGNORECASE)
        if json_match:
            return json_match.group(1).strip()
        
        # Look for JSON-like structure
        json_match = re.search(r'\{.*\}', output, re.DOTALL)
        if json_match:
            return json_match.group().strip()
        
    elif content_type == "python":
        # Look for Python in code blocks
        python_match = re.search(r'```python\s*(.*?)\s*```', output, re.DOTALL | re.IGNORECASE)
        if python_match:
            return python_match.group(1).strip()
        
        # Look for code block without language specified
        code_match = re.search(r'```\s*(.*?)\s*```', output, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
            
    elif content_type == "regex":
        # Look for regex in code blocks or inline
        regex_match = re.search(r'```regex\s*(.*?)\s*```', output, re.DOTALL | re.IGNORECASE)
        if regex_match:
            return regex_match.group(1).strip()
        
        # Look for pattern between forward slashes
        regex_match = re.search(r'/(.*?)/', output)
        if regex_match:
            return regex_match.group(1).strip()
        
        # Look for standalone pattern (common regex patterns)
        regex_match = re.search(r'([\\^$.*+?{}()|[\]]+)', output)
        if regex_match:
            return regex_match.group(1).strip()
    
    return output.strip()  # Return full output if no specific pattern found


def code_grader(output, test_case):
    """Grade the output based on code validation"""
    content_type = test_case.get("type", "").lower()
    
    if not content_type or content_type not in ["json", "python", "regex"]:
        return {
            "score": 5,  # Neutral score for unknown type
            "feedback": "Unknown content type - cannot validate"
        }
    
    # Extract relevant content
    extracted_content = extract_content_by_type(output, content_type)
    
    # Validate based on type
    if content_type == "json":
        score, feedback = validate_json(extracted_content)
    elif content_type == "python":
        score, feedback = validate_python(extracted_content)
    elif content_type == "regex":
        score, feedback = validate_regex(extracted_content)
    
    return {
        "score": score,
        "feedback": feedback,
        "extracted_content": extracted_content
    }


def create_enhanced_prompt(test_case):
    """Create prompt that specifies the expected output format"""
    content_type = test_case.get("type", "").lower()
    task = test_case["task"]
    
    format_instructions = {
        "json": "Please provide only the JSON output, properly formatted.",
        "python": "Please provide only the Python code, properly formatted in a code block.",
        "regex": "Please provide only the regex pattern."
    }
    
    instruction = format_instructions.get(content_type, "Please provide your solution.")
    
    prompt = f"""
Please solve the following task:
{task}

{instruction}
"""
    return prompt


def run_prompt(test_case):
    prompt = create_enhanced_prompt(test_case)
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
    """Grade using AI model evaluation"""
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {test_case["task"]}
    Expected Type: {test_case.get("type", "unknown")}
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
        user_input=None,
        system=[{"type": "text", "text": "You are a helpful assistant."}],
        max_tokens=500,
        stream=False,
        stop_sequences=[]
    )
    
    try:
        answer_text = evaluation.get('answer', '')
        
        if answer_text:
            cleaned = answer_text.strip()
            json_match = re.search(r'\{.*\}', cleaned, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
            else:
                parsed = json.loads(cleaned)
            
            return {
                "score": parsed.get("score", 1),
                "reasoning": parsed.get("reasoning", "No reasoning provided"),
                "strengths": parsed.get("strengths", parsed.get("strength", [])),
                "weaknesses": parsed.get("weaknesses", parsed.get("weakness", []))
            }
            
    except Exception as e:
        print(f"Error processing model evaluation: {e}")
    
    return {
        "score": 1,
        "reasoning": "Failed to parse model evaluation response",
        "strengths": [],
        "weaknesses": ["Model evaluation parsing failed"]
    }


def merge_scores(model_grade, code_grade):
    """Merge scores from model grader and code grader"""
    model_score = model_grade["score"]
    code_score = code_grade["score"]
    
    # Weighted average: 60% model grade, 40% code validation
    final_score = (model_score * 0.6) + (code_score * 0.4)
    
    return {
        "final_score": round(final_score, 2),
        "model_score": model_score,
        "code_score": code_score,
        "breakdown": {
            "model_weight": 0.6,
            "code_weight": 0.4
        }
    }


def run_test_case(test_case):
    """Run a single test case with both model and code evaluation"""
    # Validate test case has required fields
    if "type" not in test_case:
        print(f"Warning: Test case missing 'type' field: {test_case.get('task', 'Unknown task')}")
        test_case["type"] = "unknown"
    
    output = run_prompt(test_case)
    
    # Get both evaluations
    model_grade = grade_by_model(test_case, output)
    code_grade = code_grader(output, test_case)
    merged_score = merge_scores(model_grade, code_grade)
    
    return {
        "output": output,
        "test_case": test_case,
        "model_evaluation": model_grade,
        "code_evaluation": code_grade,
        "merged_score": merged_score,
        "final_score": merged_score["final_score"]
    }


def run_eval(dataset):
    """Run evaluation on entire dataset"""
    results = []
    for i, test_case in enumerate(dataset):
        print(f"Running test case {i+1}/{len(dataset)}")
        result = run_test_case(test_case)
        results.append(result)
    
    # Calculate average scores
    avg_final_score = sum(r["final_score"] for r in results) / len(results)
    avg_model_score = sum(r["model_evaluation"]["score"] for r in results) / len(results)
    avg_code_score = sum(r["code_evaluation"]["score"] for r in results) / len(results)
    
    print(f"\n=== SCORE SUMMARY ===")
    print(f"Average Final Score: {avg_final_score:.2f}")
    print(f"Average Model Score: {avg_model_score:.2f}")
    print(f"Average Code Validation Score: {avg_code_score:.2f}")
    
    return results


if __name__ == "__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
    
    results = run_eval(dataset)
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Print detailed summary
    print("\n=== DETAILED EVALUATION SUMMARY ===")
    for i, result in enumerate(results):
        print(f"\nTest {i+1}:")
        print(f"  Task: {result['test_case']['task'][:60]}...")
        print(f"  Type: {result['test_case'].get('type', 'unknown')}")
        print(f"  Final Score: {result['final_score']}/10")
        print(f"  Model Score: {result['model_evaluation']['score']}/10")
        print(f"  Code Score: {result['code_evaluation']['score']}/10")
        print(f"  Code Feedback: {result['code_evaluation']['feedback']}")
        print(f"  Model Reasoning: {result['model_evaluation']['reasoning']}")
        if result['model_evaluation']['strengths']:
            print(f"  Strengths: {', '.join(result['model_evaluation']['strengths'])}")
        if result['model_evaluation']['weaknesses']:
            print(f"  Weaknesses: {', '.join(result['model_evaluation']['weaknesses'])}")