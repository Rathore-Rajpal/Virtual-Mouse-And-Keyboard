import pyautogui as autogui
import time

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
        time.sleep(2)  # Wait for Sticky Notes to open

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

# Example usage:
take_note("This is a test note using pyautogui.")
