import time
import pyttsx3
import speech_recognition as sr
import eel
import os

@eel.expose 
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174) 
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning")
        eel.DisplayMessage('Listning...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print("recgnozing")
        eel.DisplayMessage('recgnozing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
        eel.DisplayMessage(query)
    
    except Exception as e:
        return ""
    
    return query.lower()

#text = takecommand()
#speak(text)

@eel.expose 
def allCommands(message=1):
    
    if message == 1:
        query = takecommand()
        print(f"Query received: {query}") # Debugging statement
    else:
        query = message
        
    try:
        

        if "open" in query:
            print("Handling 'open' command")  # Debugging statement
            from assist.Engine.features import openCommand
            openCommand(query)
            
        elif "on youtube" in query:
            from assist.Engine.features import PlayYoutube
            PlayYoutube(query)
            
        elif "send message" in query or "send a message" in query or "call" in query or "video call" in query:
            print("Handling WhatsApp command")  # Debugging statement
            from assist.Engine.features import findContact, whatsApp
            flag = ""

            # Call findContact and print result
            contact_no, name = findContact(query)
            print(f"Contact number: {contact_no}, Name: {name}")  # Debugging statement

            if contact_no != 0:
                if "send message" in query or "send a message" in query:
                    flag = 'message'
                    speak("What message to send?")
                    query = takecommand()
                    print(f"Message to send: {query}")  # Debugging statement
                    
                elif "phone call" in query or "make a call" in query:
                    flag = 'call'
                    
                elif "video call" in query:
                    flag = 'video call'

                # Call whatsApp method and print status
                print(f"Calling whatsApp() with number: {contact_no}, message: {query}, flag: {flag}, name: {name}")
                whatsApp(contact_no, query, flag, name)
            else:
                print("Contact not found!")  # Debugging statement

        else:
            print("Command not recognized")  # Debugging statement

    except Exception as e:
        print(f"Error in allCommands: {e}")  # Detailed error message for debugging
        
    eel.ShowHood()  # Ensure this is called even if an error occurs



