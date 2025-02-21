import os
import eel

# Initialize eel with the correct path to the 'www' folder
eel.init("assist/www")

# Launch Microsoft Edge in app mode
os.system('start msedge.exe --app="http://localhost:8000/index.html"')

# Start the Eel server and ensure block is passed as a boolean
eel.start('index.html', mode=None, host='localhost', port=8000, block=True)
