
import eel
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Engine.commands import speak



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="6d14481136d1487ba4145dd6b2287906",  # Replace with your Spotify Client ID
    client_secret="dbbf5b322810410a9c53d411f29bd095",  # Replace with your Spotify Client Secret
    redirect_uri="http://localhost:8888/callback",  # Replace with your redirect URI
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

@eel.expose
def playSpotifyMusic(query):
    try:
        # Extract the song name from the query
        song_name = query.replace("play", "").strip()
        
        # Search for the track on Spotify
        results = sp.search(q=song_name, type='track', limit=1)
        track_uri = results['tracks']['items'][0]['uri']  # Get the URI of the first track

        # Get the user's devices (where the music can be played)
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']  # Use the first available device

            # Start playback on the device
            sp.start_playback(device_id=device_id, uris=[track_uri])

            # Announce the song being played
            song_name = results['tracks']['items'][0]['name']
            artist_name = results['tracks']['items'][0]['artists'][0]['name']
            print(f"Playing {song_name} by {artist_name} on Spotify")
        else:
            print("No active devices found on Spotify")
    
    except Exception as e:
        print(f"Error in playSpotifyMusic: {e}")
        #speak("Sorry, I couldn't play the song on Spotify.")
        

playSpotifyMusic("play prove them wrong")


