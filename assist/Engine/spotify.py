import json
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import webbrowser
import assist.Engine.commands as cm
import pyautogui
import time
import psutil

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
    return {"Authorization" : "Bearer " + token}

def search_for_song(token, song_name, artist_name=None):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    
    # If artist_name is provided, search with both song name and artist name; otherwise, just the song name
    if artist_name:
        query = f"?q=track:{song_name} artist:{artist_name}&type=track&limit=1"
    else:
        query = f"?q=track:{song_name}&type=track&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    
    if result.status_code != 200:
        print(f"Error fetching the song: {result.status_code}")
        return None
    
    json_result = json.loads(result.content)["tracks"]["items"]
    
    if len(json_result) == 0:
        print(f"No track with the name '{song_name}'" + (f" by '{artist_name}'" if artist_name else "") + " found.")
        return None
    
    # Return the first track from the search results
    return json_result[0]

def play_song_on_spotify(song):
    # Open the song URL in the default web browser
    webbrowser.open(song['external_urls']['spotify'])
    cm.speak(f"Playing '{song['name']}' by {song['artists'][0]['name']} on Spotify.")
    print(f"Playing '{song['name']}' by {song['artists'][0]['name']} on Spotify.")

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    
    # Create a query for searching the artist
    query = f"?q=artist:{artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    
    if result.status_code != 200:
        print(f"Error fetching the artist: {result.status_code}")
        return None
    
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print(f"No artist with the name '{artist_name}' found.")
        return None
    
    # Return the first artist from the search results
    return json_result[0]

def open_artist_page_on_spotify(artist):
    # Open the artist's Spotify page in the default web browser
    webbrowser.open(artist['external_urls']['spotify'])
    cm.speak(f"Opening Spotify page for '{artist['name']}'")
    print(f"Opening Spotify page for '{artist['name']}'")

def handle_query(token, query):
    # Extract song name, artist name, or artist page request from the query
    if "play" in query.lower():
        # Assuming the query format is either "play {song_name} by {artist_name} on spotify"
        # or "play {song_name} on spotify"
        query = query.lower().replace("play", "").replace("on spotify", "").strip()
        
        # Check if the artist name is provided using "by"
        if "by" in query:
            song_name, artist_name = map(str.strip, query.split("by"))
        else:
            song_name = query
            artist_name = None  # No artist name provided
        
        # Search for the song on Spotify
        song = search_for_song(token, song_name, artist_name)
        
        # If song found, play it on Spotify
        if song:
            play_song_on_spotify(song)
        else:
            cm.speak("Song not found")
            print("Song not found.")
    elif "open" in query.lower() and "on spotify" in query.lower():
        # Assuming the query format is "open {artist_name} on spotify"
        query = query.lower().replace("open", "").replace("on spotify", "").strip()
        artist_name = query
        
        # Search for the artist on Spotify
        artist = search_for_artist(token, artist_name)
        
        # If artist found, open the Spotify page
        if artist:
            open_artist_page_on_spotify(artist)
        else:
            cm.speak("Artist not found")
            print("Artist not found.")
    else:
        cm.speak("Invalid query format. Use: 'play {song_name} by {artist_name} on spotify' or 'open {artist_name} on spotify'")
        print("Invalid query format. Use: 'play {song_name} by {artist_name} on spotify' or 'open {artist_name} on spotify'")


        
def play_pause():
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('spotify')
    time.sleep(1)
    pyautogui.press('enter')
    
    program_name = "Spotify.exe"
    
    timeout = time.time() + 120 #120s = 2 mins
    while True:
        for process in psutil.process_iter():
            try:
                if process.name() == program_name:
                    print("spotify is open")
                    break
               
            except(psutil.NoSuchProcess,psutil.AccessDenied):
                pass
        else:
            #if the program is not open, check if we have a timeoout
            if time.time() > timeout:
                print("timed out")
                break
            else:
                #wait for a short amout of time, before checking again
                time.sleep(1)
                continue
        #if we reach at this point, the program is open so break out of loop
        break
                
    time.sleep(7)
    pyautogui.press('space') #play music
