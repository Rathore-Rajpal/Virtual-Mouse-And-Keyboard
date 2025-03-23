import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import base64

# Load environment variables from .env file
load_dotenv()

# API configuration
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
api_key = os.getenv("HuggingFaceApiKey")
if not api_key:
    raise ValueError("API key not found in .env file")

headers = {"Authorization": f"Bearer {api_key}"}

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({"error": "Failed to generate image"}), response.status_code

    # Load image data from the response
    image_bytes = BytesIO(response.content)
    image = Image.open(image_bytes)

    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Return the base64 image string
    return jsonify({"image": f"data:image/jpeg;base64,{img_str}"})

if __name__ == '__main__':
    app.run(debug=True)