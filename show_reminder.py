
import time
from plyer import notification

notification.notify(
    title="Reminder",
    message="there is a meeting",
    timeout=10
)
