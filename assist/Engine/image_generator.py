import requests
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# API configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
api_key = os.getenv("HuggingFaceApiKey")
if not api_key:
    raise ValueError("API key not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}

# Function to send a prompt to Hugging Face API and generate images
def generate_image(prompt: str, output_path=None):

    folder_path = r"assist/Engine/Data"
    os.makedirs(folder_path, exist_ok=True)

    if output_path is None:
        output_path = os.path.join(folder_path, f"{prompt.replace(' ', '_')}.jpg")
    
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}  # Wait for the model to be ready if it isn't already
    }
    
    print(f"Generating image for prompt: '{prompt}'...")

    # Send the request to Hugging Face API
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to generate image: {response.status_code}, {response.text}")
    
    # Load image data from the response
    image_bytes = BytesIO(response.content)
    image = Image.open(image_bytes)
    
    # Save the generated image
    image.save(output_path)
    print(f"Image saved as {output_path}")

    # Open the generated image
    image.show()
    



