from groq import Groq
import json
from decouple import config

Secret_key = config("GROQ_API_KEY")

content = 'from fastapi import FastAPI\nfrom typing import Optional\nfrom pydantic import BaseModel\n\n\napp = FastAPI()\n\nclass AnalyzePRRequest(BaseModel):\n    repo_url : str\n    pr_number : int\n    github_token : Optional[str] = None\n\n\nasync def start_task_request(task_request : AnalyzePRRequest):\n    data = {\n        "repo_url" : task_request.repo_url,\n        "pr_number" : task_request.pr_number,\n        "github_token" : task_request.github_token,\n\n     }\n    print(data)\n    return {"task_id":"12", "status": "Task initiated!"}\n\n\n\nimport random\n\ndef guess_number():\n    secret_number = random.randint(1, 100)\n    attempts = 0\n    print("I\'m thinking of a number between 1 and 100.")\n\n    while True:\n        try:\n            guess = int(input("Enter your guess: "))\n            attempts += 1\n            \n            if guess < secret_number:\n                print("Too low! Try again.")\n            elif guess > secret_number:\n                print("Too high! Try again.")\n            else:\n                print(f"Correct! You found it in {attempts} attempts.")\n                break\n        except ValueError:\n            print("Please enter a valid number.")\n\nif __name__ == "__main__":\n    guess_number()\n'


import json
import re




def analyze_code_with_llm(file_content, file_name):
    #print("inside llm")
    prompt = f"""
            Analyze the following code for:
            1. code style and formatting/indentation issues.
            2. Potential bugs or errors.
            3. Performance improvements
            4. Best Practices
            
            File : {file_name}
            Content : {file_content}
            
            Provide a detailed JSON output with the following structure
            {{
                "issues" :[
                {{
                "type": "<style|bugs|performance|best_practice>",
                "line" : <line_number>,
                "description" : "<description>",
                "suggestion" : "<suggestion>"
                }}]
            }} json """
    
    client = Groq(
        api_key = Secret_key
    )
    completion = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = [
            {
                "role" : "user",
                "content" : prompt ,
            },   
        ],
        temperature = 0,
        top_p=1,
        stream=False,
        stop=None
    )

    full_response = ""
    for chunk in completion:
        delta = chunk.choices[0].delta.content
        if delta:
            full_response += delta

    # Return as JSON
    #print("full---->>>>", full_response)
    # Extract JSON inside ```json ... ``` if present
    json_match = re.search(r"```json(.*?)```", full_response, re.DOTALL)
    if json_match:
        json_text = json_match.group(1).strip()
    else:
        json_text = full_response.strip()

    # Convert to Python dict
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        # fallback if LLM output is not valid JSON
        data = {"issues": []}

    return data
    

#analyze_code_with_llm(content, "new.py")
#celery cmd --> celery -A django_app  worker -l info --pool=solo