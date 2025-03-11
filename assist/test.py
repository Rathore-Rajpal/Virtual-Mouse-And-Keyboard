import time
import psutil
import pyautogui


def play_pause():
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('spotify')
    time.sleep(1)
    pyautogui.press('enter')
    
    program_name = "Spotify.exe"
    
    timeout = time.time() + 120 #120s = 2 mins
    while True:
        for process in psutil.process_iter():
            try:
                if process.name() == program_name:
                    print("spotify is open")
                    break
               
            except(psutil.NoSuchProcess,psutil.AccessDenied):
                pass
        else:
            #if the program is not open, check if we have a timeoout
            if time.time() > timeout:
                print("timed out")
                break
            else:
                #wait for a short amout of time, before checking again
                time.sleep(1)
                continue
        #if we reach at this point, the program is open so break out of loop
        break
                
    time.sleep(7)
    pyautogui.press('space') #play music
    
play_pause()