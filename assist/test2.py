import json
from dotenv import load_dotenv 
import os
import base64
from requests import post

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_sec = os.getenv("CLIENT_SECRET")

def get_token():
    # Create authorization string
    auth_string = client_id + ":" + client_sec
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    # Spotify API token URL
    url = "https://accounts.spotify.com/api/token"
    
    # Set headers and data
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    
    # Send POST request
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    
    # Get the access token
    token = json_result.get("access_token")
    return token

def get_auth_header(token):
    return {"Autheroization: " : "Bearer "+ token}
    
# Call the get_token function
tokens = get_token()
print(tokens)
