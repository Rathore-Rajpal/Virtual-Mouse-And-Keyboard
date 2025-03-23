import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API configuration for code generation model (using BigCode's StarCoder)
CODE_API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
api_key = os.getenv("HuggingFaceApiKey")
if not api_key:
    raise ValueError("API key not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}

def generate_code(task_prompt: str):
    payload = {
        "inputs": f"<fim_prefix># Python\n# {task_prompt}\n<fim_suffix>\n<fim_middle>",
        "parameters": {
            "temperature": 0.9,
            "max_new_tokens": 256,
            "return_full_text": False
        }
    }

    print(f"Generating code for prompt: '{task_prompt}'...")

    response = requests.post(CODE_API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Code generation failed: {response.status_code}, {response.text}")

    generated_code = response.json()[0]['generated_text']
    
    # Post-processing to clean up the output
    generated_code = generated_code.split("<|endoftext|>")[0].strip()
    
    return generated_code  # Return the generated code instead of saving to a file
