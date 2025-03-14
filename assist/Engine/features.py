import random
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
import random
from datetime import datetime
from plyer import notification
import sys
from assist.Engine.commands import takecommand
import psutil




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
    
@eel.expose
def playChatSound():
    mis_dir = "C:\\VirtualMouseProject\\assist\\www\\assets\\audio\\chat_sound.wav"
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
    
import webbrowser

def SearchYoutube(query):
    search_term = query.lower().replace("search", "").replace("on youtube", "").strip()
    search_url = f"https://www.youtube.com/results?search_query={search_term}"
    speak(f"searching for {search_term} on youtube")
    webbrowser.open(search_url)
    
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


def chatBot(query):
    global stop_flag
    user_input = query.lower()
    
    chatbot = hugchat.ChatBot(cookie_path="assist\\Engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    
    return response

        
def google_search(query):
     search_term = query.replace("search", "").replace("on google", "").replace("on internet", "").strip()
     speak(f"Searching for {search_term} on Google")
     search_url = f"https://www.google.com/search?q={search_term}"
     webbrowser.open(search_url)
     
def take_note(note):
    try:
        # Open Start Menu
        autogui.press('win')
        time.sleep(1)

        # Search for Sticky Notes
        autogui.write('Sticky Notes')
        time.sleep(1)

        # Press Enter to open Sticky Notes
        autogui.press('enter')
        time.sleep(3)  # Wait for Sticky Notes to open

        # Press Tab 4 times to focus on the area where you can add a new note
        for _ in range(4):
            autogui.press('tab')
            time.sleep(0.3)  # Slight delay between each tab press

        # Press Enter to create a new note
        autogui.press('enter')
        time.sleep(1)  # Wait for the new note to appear

        # Write the note
        autogui.write(note)
        time.sleep(1)
        
        for _ in range(7):
            autogui.press('tab')
            time.sleep(0.3)
            
        autogui.press('enter')
        time.sleep(1)

        #Optionally, close the Sticky Notes window
        autogui.hotkey('alt', 'f4')  # Closes the Sticky Notes window

        print("Note successfully added!")
    
    except Exception as e:
        print(f"An error occurred while taking the note: {e}")

def caputure_screenshot():
    time.sleep(2)
    autogui.hotkey('win','down')
    folder_path = 'C:\\VirtualMouseProject\\Screeshots'
    time.sleep(1)
    img = autogui.screenshot()
    time.sleep(1)
    label = random.randint(1, 1000)
    img.save(os.path.join(folder_path, f'my_screenshot_{label}.png'))
    

def create_python_script(subject):
    python_script_content = f'''
import time
from plyer import notification

notification.notify(
    title="Reminder",
    message="{subject}",
    timeout=10
)
'''
    python_script_path = os.path.join(os.getcwd(), "show_reminder.py")
    with open(python_script_path, "w") as file:
        file.write(python_script_content)
    return python_script_path

def set_reminder(reminder_datetime, subject):
    date_format = reminder_datetime.strftime("%d/%m/%Y")
    time_format = reminder_datetime.strftime("%H:%M")
    
    python_script_path = create_python_script(subject)
    pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
    
    if not os.path.isfile(pythonw_path):
        raise FileNotFoundError("pythonw.exe not found. Ensure Python is installed correctly.")
    
    command = (
        f'schtasks /create /tn "Reminder_{subject}" '
        f'/tr "\"{pythonw_path}\" \"{python_script_path}\"" '
        f'/sc once /st {time_format} /sd {date_format} /f'
    )
    
    os.system(command)
    
    # Print formatted date and time
    print(f"Reminder set for {date_format} at {time_format} - {subject}")
    
@eel.expose
def processEmailDetails(name, email, subject):
    try:
        if name and email and subject:
            # Open Gmail compose window with recipient email and subject
            compose_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}"
            webbrowser.open(compose_url)
            speak(f"Composing an email to {name} with subject: {subject}")
        else:
            speak("Please provide all the required details.")
    except Exception as e:
        print(f"Error in processing email: {e}")
        speak("An error occurred while processing the email.")


def send_email(query):
    speak("Whom do you want to send the email to?")
    recipient_name = takecommand().lower()
    
    cursor.execute("SELECT email FROM contacts WHERE LOWER(name) = ?", (recipient_name,))
    result = cursor.fetchone()
    print(result)

    if result:
        email = result[0]
        speak(f"Found {recipient_name}'s email: {email}. What should be the subject?")
        subject = takecommand()

        # Open Gmail compose window with recipient email and subject
        compose_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={subject}"
        webbrowser.open(compose_url)
        speak(f"Composing an email to {recipient_name} with subject: {subject}")
    
    else:
        # If no contact found, prompt the user to input details via the HTML form
        eel.toggleEmailSection(True)
        speak(f"No email found for {recipient_name}. Please provide the details manually.")
        
def close_app(query):
    # Extract the app name from the query
    app_name = query.lower().replace("close ", "").strip()

    # Check if the app is open
    is_running = False
    for process in psutil.process_iter(['pid', 'name']):
        if app_name in process.info['name'].lower():
            is_running = True
            pid = process.info['pid']
            print(f"Closing {app_name} (PID: {pid})...")
            
            # Terminate the app
            try:
                os.kill(pid, 9)  # 9 is the signal for termination
                print(f"{app_name} closed successfully.")
                speak(f"{app_name} closed successfully.")
            except Exception as e:
                print(f"Error occurred while closing {app_name}: {e}")
            break
    
    if not is_running:
        speak(f"{app_name} is not running.")
        print(f"{app_name} is not running.")
   




