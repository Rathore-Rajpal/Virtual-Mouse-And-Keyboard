from playsound import playsound
import eel
from assist.Engine.config import ASSISTANT_NAME
import os

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