import os
import psutil
from assist.Engine.commands import speak

def close_app(query):
    # Extract the app name from the query
    app_name = query.lower().replace("close ", "").strip()

    # Print all currently running apps
    print("Currently running apps:")
    for process in psutil.process_iter(['pid', 'name']):
        print(f"App Name: {process.info['name']} (PID: {process.info['pid']})")

close_app("close notepad")
    
