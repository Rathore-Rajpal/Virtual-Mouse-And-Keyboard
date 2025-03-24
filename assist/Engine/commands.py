import subprocess
import sys
import time
import webbrowser
import dateparser
import keyboard
import pyttsx3
import speech_recognition as sr
import eel
import os
import assist.Engine.spotify as sp
import pyautogui as auto

@eel.expose
def speak(text):
    text = str(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage('Listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print("Recognizing...")
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
        eel.DisplayMessage(query)
    
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(f"Query received: {query}")  # Debugging statement
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
        
    try:
        # Handle Spotify command first if it matches the format "open {artist_name} on Spotify"
        if "open" in query and "on spotify" in query:
            print("Handling 'open artist on Spotify' command")
            token = sp.get_token()
            sp.handle_query(token, query)
        
        # General "open" command
        elif "open" in query:
            print("Handling general 'open' command")
            from assist.Engine.features import openCommand
            openCommand(query)
        
        elif "on youtube" in query:
            if "search" in query:
                from assist.Engine.features import SearchYoutube
                SearchYoutube(query)
            else:
                from assist.Engine.features import PlayYoutube
                PlayYoutube(query)
        
        elif any(kw in query for kw in ["send message", "voice call", "video call", "send a message","call"]):
            print("Handling WhatsApp command")
            from assist.Engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            print(f"Contact number: {contact_no}, Name: {name}")
            
            if contact_no != 0:
                if "send message" in query or "send a message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    query = takecommand()
                    print(f"Message to send: {query}")
                
                elif "phone call" in query or "call" in query or "voice call" in query:
                    flag = 'call'
                
                elif "video call" in query:
                    flag = 'video call'
                
                print(f"Calling whatsApp() with number: {contact_no}, message: {query}, flag: {flag}, name: {name}")
                whatsApp(contact_no, query, flag, name)
            else:
                print("Contact not found!")
                
        elif "search" in query:
            if "on google" in query or "on internet" in query:
                print("Handling 'search on Google' command")
                from assist.Engine.features import google_search
                google_search(query)
            else:
                print("Handling 'product search on website' command")
                from assist.Engine.searchingProduct import search_product
                search_product(query)
        
        elif "on spotify" in query or "play on spotify" in query:
            print("Handling 'Spotify' command")
            token = sp.get_token()
            sp.handle_query(token, query)
        
        elif "take a note" in query and "in file" not in query:
            print("Handling 'take a note' command")
            speak("What would you like to note down?")
            note = takecommand()
            if note:
                from assist.Engine.features import take_note
                take_note(note)
                speak("Your note has been saved.")
            else:
                speak("I couldn't hear the note properly. Please try again.")
        
        elif "take a note in file" in query or "write a note in file" in query:
            print("Handling 'take a note in file' command")
            speak("What would you like to note down?")
            note = takecommand()
            if note:
                with open("sticky_notes.txt", "a") as file:
                    file.write(note + "\n")
                speak("Your note has been saved to the file.")
            else:
                speak("I couldn't hear the note properly. Please try again.")
        
        elif "some music" in query or "play music" in query:
            speak("Playing some music for you")
            print("Handling 'music play' command")
            sp.play_pause()
        
        elif "screenshot" in query.lower():
            from assist.Engine.features import caputure_screenshot
            speak("capturing screenshot")
            caputure_screenshot()
            speak("Screenshot captured sucessfully")
            
        elif "set a reminder" in query:
            from assist.Engine.features import set_reminder
            speak("Please tell me when you want to set the reminder.'.")
            reminder_input = takecommand()

            speak("What is the reminder about?")
            reminder_subject = takecommand()

            # Use dateparser to parse natural language input into a datetime object
            reminder_datetime = dateparser.parse(reminder_input)
            
            if reminder_datetime:
                set_reminder(reminder_datetime, reminder_subject)
                speak(f"Your reminder for {reminder_subject} is set for {reminder_datetime}.")
            else:
                speak("Sorry, I couldn't understand the date and time. Please try again.")
                
        elif ("send a email" in query or "send email" in query or "send a mail" in query or "send an email" in query or "draft a mail" in query):
            from assist.Engine.features import send_email
            send_email(query)
            
        elif "close" in query or "terminate" in query:
            from assist.Engine.features import close_app
            close_app(query)
            
        elif "bye-bye" in query.lower():
            speak("Terminating the assistant...")
            auto.hotkey('alt','f4')
            
        elif "generate image" in query or "generate an image" in query:
            from assist.Engine.image_generator import generate_image
            speak("What image you need to generate: ")
            prompt = takecommand()
            speak(f"Generating image:{prompt}")
            generate_image(prompt)
            speak("Image Generated Sucessfully")
            
        elif "search for " in query:
            from assist.Engine.searchingProduct import search_product
            search_product(query)
            
        elif "write a code" in query or "generate a code" in query or "write the code" in query:
            from assist.Engine.features import codeBot
            codeBot(query)
            
        elif "shortest route" in query or "shortest distance" in query or "google maps" in query or "maps" in query or "distance" in query:
            from assist.Engine.features import open_shortest_route
            open_shortest_route(query)
        
        elif "start image master" in query or "lauch image master" in query:
            speak("Launching Image Master")
            eel.ShowHood()
            file_path = r'assist\Engine\ImageBot\index.html'
            webbrowser.open(file_path)
            python_interpreter = r'C:\VirtualMouseProject\envjarvis\Scripts\python.exe'
            subprocess.Popen([python_interpreter, r'assist\Engine\ImageBot\app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            
        elif "start code master" in query or "launch code master" in query:
            speak("Launching Code Master")
            eel.ShowHood()
            file_path = r'assist\Engine\CodingBuddy\index.html'
            webbrowser.open(file_path)
            python_interpreter = r'C:\VirtualMouseProject\envjarvis\Scripts\python.exe'
            subprocess.Popen([python_interpreter, r'assist\Engine\CodingBuddy\app.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
        elif "start virtual mouse" in query or "launch virtual mouse" in query:
            speak("Launching virtual mouse")
            eel.ShowHood()
            subprocess.run(['python','virtualMouse.py'])

            
        elif "start virtual keyboard" in query or "launch virtual keyboard" in query:
            speak("Starting virtual keyboard")
            eel.ShowHood()
            subprocess.run(['python','virtual_ketboard.html.py'])
            
        elif "conatcts table" in query:
            eel.toggleContactsSection(True)
            
        else:
            speak("This command is forwarded to AI bot, do you want to continue?")
            confirmation = takecommand()
            print(confirmation)
            if "yes" in confirmation or "sure" in confirmation or "okay" in confirmation:
                eel.DisplayMessage("Handling 'AI Bot' command")
                print("Handling 'AI Bot' command")
                from assist.Engine.features import chatBot
                # Direct call pattern like codeBot
                chatBot(query)
            else:
                speak("Okay, let me know if you need anything else.")
    except Exception as e:
        print(f"Error in allCommands: {e}")  # Detailed error message for debugging

    eel.ShowHood()  # Ensure this is called even if an error occurs
