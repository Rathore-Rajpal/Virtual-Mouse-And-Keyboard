import re
import sqlite3
import struct
import time
import webbrowser
from playsound import playsound
import eel
import pyautogui
from assist.Engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit 
from assist.Engine.commands import speak
from assist.Engine.helper import extract_yt_term
import pvporcupine
import pyaudio

#playing assistant sound function.
conn = sqlite3.connect("buddy.db")
cursor = conn.cursor()

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

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)
    
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    
    try:
        # Initialize Porcupine without access_key (as it's not needed in this version)
        porcupine = pvporcupine.create(
            keywords=["jarvis", "alexa"],  # List of keywords to detect
            sensitivities=[0.4, 0.4]  # Sensitivity for better detection accuracy
        )

        paud = pyaudio.PyAudio()
        
        
        # Use default input device or specify index manually
        input_device_index = None  # Set to None for default, or specify an index from list_microphones
        
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=input_device_index,  # Set microphone input device
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotwords...")

        # Hotword detection loop
        while True:
            try:
                pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                
                # Detect keyword
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    detected_word = ["jarvis", "alexa"][keyword_index]
                    print(f"Hotword detected: {detected_word}")
                    
                    # Simulate keypress (Win+J)
                    pyautogui.keyDown("alt")
                    pyautogui.press("j")
                    time.sleep(0.1)
                    pyautogui.keyUp("alt")
                    time.sleep(1)  # Cooldown to prevent multiple detections

            except IOError as e:
                print("Audio read error:", e)
                continue

    except Exception as e:
        print("Error:", e)
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()