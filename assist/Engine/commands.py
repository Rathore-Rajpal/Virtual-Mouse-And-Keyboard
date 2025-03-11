import time
import pyttsx3
import speech_recognition as sr
import eel
import os
import assist.Engine.spotify as sp

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
        if "open" in query:
            print("Handling 'open' command")
            from assist.Engine.features import openCommand
            openCommand(query)
        
        elif "on youtube" in query:
            from assist.Engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif any(kw in query for kw in ["send message", "call", "video call"]):
            print("Handling WhatsApp command")
            from assist.Engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            print(f"Contact number: {contact_no}, Name: {name}")
            
            if contact_no != 0:
                if "send message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    query = takecommand()
                    print(f"Message to send: {query}")
                
                elif "phone call" in query:
                    flag = 'call'
                
                elif "video call" in query:
                    flag = 'video call'
                
                print(f"Calling whatsApp() with number: {contact_no}, message: {query}, flag: {flag}, name: {name}")
                whatsApp(contact_no, query, flag, name)
            else:
                print("Contact not found!")
                
        elif "search" in query and ("on google" in query or "on internet" in query):
            print("Handling 'search on Google' command")  # Debugging statement
            from assist.Engine.features import google_search
            google_search(query)
        
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
            print("Handling 'music play' command")
            sp.play_pause()
        
        else:
            from assist.Engine.features import chatBot
            chatBot(query)
    
    except Exception as e:
        print(f"Error in allCommands: {e}")  # Detailed error message for debugging

    eel.ShowHood()  # Ensure this is called even if an error occurs
