import subprocess
import time
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import Timings

# Configure UI response times
Timings.defaults()

def open_clock_app():
    """Open Windows Clock app and bring to foreground"""
    app = None
    try:
        # Try to connect to running instance
        app = Application(backend="uia").connect(class_name="ApplicationFrameWindow")
    except ElementNotFoundError:
        try:
            # Start new instance if not running
            subprocess.Popen(r"explorer shell:AppsFolder\Microsoft.WindowsAlarms_8wekyb3d8bbwe!App")
            time.sleep(5)  # Increased wait time for app launch
            
            # Try connecting again
            app = Application(backend="uia").connect(class_name="ApplicationFrameWindow")
        except Exception as e:
            raise RuntimeError("Failed to start Clock app") from e
    
    # Verify window exists
    if not app.window(title_re=".*Alarms.*Clock.*").exists():
        raise RuntimeError("Clock app window not found")
    
    return app.window(title_re=".*Alarms.*Clock.*")

def set_windows_alarm(hours, minutes, am_pm="AM", alarm_name="Python Alarm"):
    """
    Set an alarm in Windows Clock app
    :param hours: int (1-12)
    :param minutes: int (0-59)
    :param am_pm: "AM" or "PM"
    :param alarm_name: Name for the alarm
    """
    try:
        app = open_clock_app()
        app.set_focus()
        
        # Navigate to Alarms tab
        alarms_tab = app.child_window(title="Alarm", control_type="TabItem")
        alarms_tab.click_input()
        time.sleep(1)
        
        # Rest of the function remains the same...
        # [Keep the original alarm setting code here]
        
    except Exception as e:
        print(f"Error setting alarm: {str(e)}")
        
def main():
    # Example usage
    set_windows_alarm(7, 30, am_pm="AM", alarm_name="Wake Up")
    #start_stopwatch()
    #set_timer(0, 25, 0, timer_name="Pomodoro Timer")

if __name__ == "__main__":
    main()