import time
import pyautogui as autogui
import os
import random
import pygetwindow as gw

def capture_screenshot():
    
    time.sleep(2)
    autogui.hotkey('win', 'down')
    folder_path = 'C:\\VirtualMouseProject\\Screenshots'
    time.sleep(1)
    img = autogui.screenshot()
    time.sleep(1)
    label = random.randint(1, 1000)
    img.save(os.path.join(folder_path, f'my_screenshot_{label}.png'))
    time.sleep(1)
    
    # Find the active window (you can change the title to the one you want to maximize)
    window = gw.getActiveWindow()
    
    if window:
        window.maximize()

# Call the function to capture the screenshot
capture_screenshot()
