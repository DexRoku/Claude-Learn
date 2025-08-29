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


def generate_html_report(results):
    """Generate an HTML report from evaluation results"""
    
    # Calculate summary statistics
    total_tests = len(results)
    avg_final_score = sum(r["final_score"] for r in results) / total_tests if total_tests > 0 else 0
    avg_model_score = sum(r["model_evaluation"]["score"] for r in results) / total_tests if total_tests > 0 else 0
    avg_code_score = sum(r["code_evaluation"]["score"] for r in results) / total_tests if total_tests > 0 else 0
    
    # Count by type
    type_counts = {}
    for result in results:
        content_type = result['test_case'].get('type', 'unknown')
        type_counts[content_type] = type_counts.get(content_type, 0) + 1
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evaluation Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary {{
            padding: 30px;
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #4a5568;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #2d3748;
        }}
        .type-breakdown {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .type-badge {{
            background: #4299e1;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        .results {{
            padding: 0;
        }}
        .test-case {{
            border-bottom: 1px solid #e2e8f0;
            padding: 25px;
            transition: background-color 0.3s;
        }}
        .test-case:hover {{
            background: #f7fafc;
        }}
        .test-case:last-child {{
            border-bottom: none;
        }}
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .test-number {{
            background: #4a5568;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .test-type {{
            background: #38b2ac;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .task-description {{
            background: #edf2f7;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-style: italic;
            color: #4a5568;
        }}
        .scores {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .score-item {{
            text-align: center;
            padding: 15px;
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
        }}
        .score-item.final {{
            border-color: #38b2ac;
            background: #e6fffa;
        }}
        .score-value {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2d3748;
        }}
        .score-label {{
            font-size: 0.8em;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }}
        .detail-section {{
            background: #f7fafc;
            padding: 15px;
            border-radius: 6px;
        }}
        .detail-section h4 {{
            margin: 0 0 10px 0;
            color: #4a5568;
            font-size: 1em;
        }}
        .detail-section p {{
            margin: 5px 0;
            color: #718096;
            line-height: 1.4;
        }}
        .strengths, .weaknesses {{
            list-style: none;
            padding: 0;
        }}
        .strengths li {{
            background: #c6f6d5;
            color: #22543d;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 4px solid #38a169;
        }}
        .weaknesses li {{
            background: #fed7d7;
            color: #742a2a;
            padding: 8px 12px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 4px solid #e53e3e;
        }}
        .output-section {{
            grid-column: 1 / -1;
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .toggle-output {{
            background: #4299e1;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        .toggle-output:hover {{
            background: #3182ce;
        }}
        .output-content {{
            display: none;
        }}
        @media (max-width: 768px) {{
            .details {{
                grid-template-columns: 1fr;
            }}
            .scores {{
                grid-template-columns: 1fr;
            }}
            .summary-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI Evaluation Report</h1>
            <p>Comprehensive analysis of {total_tests} test cases</p>
        </div>
        
        <div class="summary">
            <div class="summary-grid">
                <div class="summary-card">
                    <h3>Final Average Score</h3>
                    <div class="value">{avg_final_score:.1f}/10</div>
                </div>
                <div class="summary-card">
                    <h3>Model Score</h3>
                    <div class="value">{avg_model_score:.1f}/10</div>
                </div>
                <div class="summary-card">
                    <h3>Code Score</h3>
                    <div class="value">{avg_code_score:.1f}/10</div>
                </div>
                <div class="summary-card">
                    <h3>Total Tests</h3>
                    <div class="value">{total_tests}</div>
                </div>
            </div>
            <div class="type-breakdown">
                {"".join([f'<span class="type-badge">{type_name}: {count}</span>' for type_name, count in type_counts.items()])}
            </div>
        </div>
        
        <div class="results">
"""

    for i, result in enumerate(results, 1):
        test_case = result['test_case']
        model_eval = result['model_evaluation']
        code_eval = result['code_evaluation']
        
        strengths_html = "".join([f"<li>{strength}</li>" for strength in model_eval['strengths']])
        weaknesses_html = "".join([f"<li>{weakness}</li>" for weakness in model_eval['weaknesses']])
        
        html_content += f"""
            <div class="test-case">
                <div class="test-header">
                    <span class="test-number">Test {i}</span>
                    <span class="test-type">{test_case.get('type', 'unknown')}</span>
                </div>
                
                <div class="task-description">
                    <strong>Task:</strong> {test_case['task']}
                </div>
                
                <div class="scores">
                    <div class="score-item final">
                        <div class="score-value">{result['final_score']}</div>
                        <div class="score-label">Final Score</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{model_eval['score']}</div>
                        <div class="score-label">Model Score</div>
                    </div>
                    <div class="score-item">
                        <div class="score-value">{code_eval['score']}</div>
                        <div class="score-label">Code Score</div>
                    </div>
                </div>
                
                <div class="details">
                    <div class="detail-section">
                        <h4>Model Reasoning</h4>
                        <p>{model_eval['reasoning']}</p>
                    </div>
                    
                    <div class="detail-section">
                        <h4>Code Validation</h4>
                        <p>{code_eval['feedback']}</p>
                    </div>
                    
                    {"<div class='detail-section'><h4>Strengths</h4><ul class='strengths'>" + strengths_html + "</ul></div>" if model_eval['strengths'] else ""}
                    
                    {"<div class='detail-section'><h4>Weaknesses</h4><ul class='weaknesses'>" + weaknesses_html + "</ul></div>" if model_eval['weaknesses'] else ""}
                    
                    <div class="output-section">
                        <button class="toggle-output" onclick="toggleOutput({i})">Toggle Output</button>
                        <div class="output-content" id="output-{i}">AI Output:
{result['output']}</div>
                    </div>
                </div>
            </div>
"""

    html_content += """
        </div>
    </div>
    
    <script>
        function toggleOutput(testId) {
            const output = document.getElementById('output-' + testId);
            if (output.style.display === 'none' || output.style.display === '') {
                output.style.display = 'block';
            } else {
                output.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""
    
    return html_content


if __name__ == "__main__":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)
    
    results = run_eval(dataset)
    
    # Save JSON results
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate and save HTML report
    html_report = generate_html_report(results)
    with open("evaluation_report.html", "w", encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"\n✅ Evaluation complete!")
    print(f"📊 JSON results saved to: evaluation_results.json")
    print(f"📄 HTML report saved to: evaluation_report.html")
    
    # Print console summary
    total_tests = len(results)
    avg_final_score = sum(r["final_score"] for r in results) / total_tests if total_tests > 0 else 0
    print(f"🎯 Average Final Score: {avg_final_score:.2f}/10 ({total_tests} tests)")
    print("\nOpen evaluation_report.html in your browser to view the detailed report!")