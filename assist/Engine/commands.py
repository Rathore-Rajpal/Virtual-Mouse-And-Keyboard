import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174) 
    print(voices)
    engine.say(text)
    engine.runAndWait()

speak("India is my counrty and all indian are my brohters and sisters")

 

