import os
import eel
import time
from assist.Engine.features import *
from assist.Engine.commands import *
from assist.Engine.auth import recoganize

def start():
    # Initialize eel with the correct path to the 'www' folder
    eel.init("assist/www")
    playAssistantSound()
    @eel.expose
    def init():
         #subprocess.call([r'device.bat'])
         #eel.hideLoader()
         #speak("Ready for face Authentication")
         #lag = recoganize.AuthenticateFace()
         flag=1
         if(flag == 1):
             #eel.hideFaceAuth()
             #speak("Face autentication sucessfull")
             #eel.hideFaceAuthSuccess()
             speak("welcome to AI Assistant. I am your buddy..ready to help")
             eel.hideStart()
             playAssistantSound()
         else:
             speak("Face autentication Failed")
        
   

    # Launch Microsoft Edge in app mode
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    # Start the Eel server and ensure block is passed as a boolean
    eel.start('index.html', mode=None, host='localhost', port=8000, block=True)
