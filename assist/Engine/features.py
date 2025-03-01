import re
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from hugchat import hugchat
from playsound import playsound
import eel
import pyautogui as autogui
from assist.Engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit 
from assist.Engine.commands import speak
from assist.Engine.helper import extract_yt_term, remove_words
import pvporcupine
import pyaudio

stop_flag = False 
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
    pa = None
    audio_stream = None

    try:
        access_key = "nm2uZzRWhxQ1MxyzsIGhOOkROeGh2WTdGQmdkOBtlaq4b9trt0YENQ=="
        keyword_path = "C:\\VirtualMouseProject\\hey-buddy_en_windows_v3_0_0\\hey-buddy_en_windows_v3_0_0.ppn"

        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path],
            sensitivities=[0.5]
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'buddy'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            
            if result >= 0:
                print("Hotword detected!")
                autogui.hotkey('alt', 'j')  # Simplified key combination
                time.sleep(1)

    except Exception as e:
        print("Error:", e)
    finally:
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if pa:
            pa.terminate()


#Find Contacts
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)
    
    try:
        # Strip and lowercase the query
        query = query.strip().lower()
        
        # Split to get the first word of the query
        first_word_query = query.split()[0]

        # Execute the SQL query to search for contacts with the first word, case-insensitive
        cursor.execute("""
            SELECT mobile_no FROM contacts 
            WHERE LOWER(SUBSTR(name, 1, LENGTH(?))) = ?
        """, (first_word_query, first_word_query))
        
        results = cursor.fetchall()

        # If a result is found, format the mobile number
        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            speak('not exist in contacts')
            return 0, 0

    except Exception as e:
        print(f"Error in findContact: {e}")
        speak('not exist in contacts')
        return 0, 0

    
def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            target_tab = 12
            jarvis_message = "Message sent successfully to " + name

        elif flag == 'call':
            target_tab = 7
            message = ''
            jarvis_message = "Calling " + name

        else:
            target_tab = 6
            message = ''
            jarvis_message = "Starting video call with " + name

        # Encode the message for URL
        encoded_message = quote(message)

        # Construct the URL
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

        # Debugging: Print the constructed URL
        print(f"Constructed WhatsApp URL: {whatsapp_url}")

        # Open WhatsApp with the constructed URL using cmd.exe
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

        # Wait for WhatsApp to open and switch to correct tab
        time.sleep(5)  # Adjust the delay as necessary
        
        # Simulate tabbing to the target option
        autogui.hotkey('ctrl', 'f')
        for i in range(1, target_tab):
            autogui.hotkey('tab')
        autogui.hotkey('enter')

        # Speak confirmation message
        speak(jarvis_message)
    
    except Exception as e:
        print(f"Error in WhatsApp function: {e}")


@eel.expose
def stopChatBot():
    global stop_flag
    stop_flag = True  # Set the flag to True to stop the conversation
    print("Chatbot conversation stopped.")
    print("Method called")

def chatBot(query):
    global stop_flag
    user_input = query.lower()
    
    if stop_flag:
        print("Process stopped. No response will be generated.")
        return
    
    chatbot = hugchat.ChatBot(cookie_path="assist\Engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    
    return response
