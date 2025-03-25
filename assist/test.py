import re
import time
import pyautogui as autogui


def call_on_mobile(query):
     pattern = r'(?:call|make a call to) ([a-zA-Z ]+) on my (?:phone|iphone)'
    
     # Search for the pattern in the query
     match = re.search(pattern, query.lower())
    
     if match:
        name = match.group(1)
        autogui.press('win')
        time.sleep(1)
        autogui.write("phone link")
        autogui.press('enter')
        time.sleep(4)
        autogui.click(500, 90,duration=1)
        for i in range(3):
            autogui.press('tab')
        autogui.write(name)
        time.sleep(1)
        autogui.press('enter')
        for i in range(13):
            autogui.press('tab')
        autogui.sleep(1)
        autogui.press('enter')
        
def message_on_phone(query):
    pattern = r'(?:message|send a message to) ([a-zA-Z ]+) (?:to|on) my (?:phone|iphone)'
    match = re.search(pattern, query.lower())
    time.sleep(1)
    message = "Hello how are you"
    if match:
        name = match.group(1)
        autogui.press('win')
        time.sleep(1)
        autogui.write("phone link")
        autogui.press('enter')
        time.sleep(4)
        autogui.click(600, 90,duration=1)
        for i in range(2):
            autogui.press('tab')
        time.sleep(1)
        autogui.press('enter')
        autogui.write(name)
        autogui.press('enter')
        time.sleep(1)
        autogui.write(message)
        autogui.press('enter')
        
#message_on_phone("send a message to sister to my phone")
call_on_mobile("make a call to sister on my phone")
    
        
  
