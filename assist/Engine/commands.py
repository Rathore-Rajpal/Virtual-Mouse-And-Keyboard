import pyttsx3
import speech_recognition as sr
import eel

@eel.expose 
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174) 
    engine.say(text)
    engine.runAndWait()

@eel.expose 
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning")
        eel.DisplayMessage('Listning...')
        r.pause_threshold= 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print("recgnozing")
        eel.DisplayMessage('recgnozing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
        eel.DisplayMessage(query)
        speak(query)
    
    except Exception as e:
        return ""
    
    return query.lower()

#text = takecommand()
#speak(text)

 

