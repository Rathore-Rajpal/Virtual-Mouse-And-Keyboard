import re
from playsound import playsound
import eel
from assist.Engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit 
from assist.Engine.commands import speak

#playing assistant sound function.

@eel.expose
def playAssistantSound():
    mis_dir = "C:\\VirtualMouseProject\\assist\\www\\assets\\audio\\start_sound.mp3"
    playsound(mis_dir)

@eel.expose
def playMicSound():
    mis_dir = "C:\\VirtualMouseProject\\assist\\www\\assets\\audio\\mic_sound.wav"
    playsound(mis_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.replace("hey", "")
    query.lower()

    if query != "":
        speak("Opening..."+query)
        os.system('start '+query)
    else:
        speak("Not found !")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    #Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    #use re.search to to find the match in the command
    match = re.search(pattern,command,re.IGNORECASE)
    #if the is found return the extracted song name; otherwise return None
    return match.group(1) if match else None
