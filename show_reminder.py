import time
from datetime import datetime
from plyer import notification

notification.notify(
    title="Reminder",
    message="Meeting with client",
    timeout=10
)
time.sleep(15)  # Keep script alive for notification
