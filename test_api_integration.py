import os
from groq import Groq
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: GROQ_API_KEY not found in .env")
    exit(1)

print(f"API Key loaded: {api_key[:10]}...{api_key[-5:] if len(api_key)>10 else ''}")

# Configure Groq
client = Groq(api_key=api_key)
model_id = 'llama-3.3-70b-versatile'

def test_generate_questions():
    print("Testing Question Generation...")
    difficulty = "intermediate"
    tech_stack = ["Python", "Streamlit"]
    
    prompt = f"""
    You are a technical interviewer.
    Generate 3 {difficulty} level interview questions for each technology listed.
    Technologies: {tech_stack}
    
    Return the output as a JSON object with a key "questions" containing a list of strings.
    Example: {{ "questions": ["Question 1", "Question 2"] }}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=model_id,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        print(f"Raw Response: {content}")
        
        data = json.loads(content)
        if "questions" in data and isinstance(data["questions"], list):
            print("[SUCCESS] Question Generation Test Passed!")
            print(f"Generated {len(data['questions'])} questions.")
        else:
            print("[FAILED] Question Generation Test Failed: Invalid JSON structure.")
            
    except Exception as e:
        print(f"[FAILED] Question Generation Test Failed with error: {str(e)}")


def test_evaluate_answer():
    print("\nTesting Answer Evaluation...")
    question = "Explain the difference between list and tuple in Python."
    answer = "Lists are mutable, tuples are immutable."
    
    eval_prompt = f"""
    Evaluate the following answer on scale 1-5 for:
    clarity, technical accuracy, depth.
    
    Question: {question}
    Answer: {answer}
    
    Return the output as a JSON object with keys: "clarity", "technical_accuracy", "depth".
    Example: {{ "clarity": 4, "technical_accuracy": 5, "depth": 3 }}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": eval_prompt}
            ],
            model=model_id,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        print(f"Raw Response: {content}")
        
        data = json.loads(content)
        required_keys = ["clarity", "technical_accuracy", "depth"]
        if all(k in data for k in required_keys):
            print("[SUCCESS] Answer Evaluation Test Passed!")
            print(f"Scores: {data}")
        else:
            print("[FAILED] Answer Evaluation Test Failed: Missing keys.")

    except Exception as e:
        print(f"[FAILED] Answer Evaluation Test Failed with error: {str(e)}")

if __name__ == "__main__":
    test_generate_questions()
    test_evaluate_answer()
