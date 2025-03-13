import datetime
import google.auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# Scopes for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Authenticate and return the Google Calendar API service."""
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'

    # Check if we already have valid credentials
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next time
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return build('calendar', 'v3', credentials=creds)

def schedule_meeting(event_summary, start_time, end_time, attendees):
    """
    Schedule a meeting on Google Calendar.
    
    :param event_summary: Title or name of the meeting.
    :param start_time: Meeting start time as ISO format string (YYYY-MM-DDTHH:MM:SS).
    :param end_time: Meeting end time as ISO format string.
    :param attendees: List of attendees' email addresses.
    """
    service = authenticate_google_calendar()
    
    event = {
        'summary': event_summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',  # Adjust timezone as necessary
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
        'attendees': [{'email': email} for email in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Email reminder 1 day before
                {'method': 'popup', 'minutes': 10},      # Popup reminder 10 minutes before
            ],
        },
    }
    
    # Insert the event into the user's calendar
    event_result = service.events().insert(calendarId='primary', body=event).execute()
    
    print(f"Meeting scheduled: {event_result.get('htmlLink')}")
    return event_result.get('htmlLink')

# Example usage
def auto_schedule_meeting():
    event_title = "Team Sync Meeting"
    start_time = '2025-03-13T10:00:00'
    end_time = '2025-03-13T11:00:00'
    attendees = ['attendee1@example.com', 'attendee2@example.com']
    
    link = schedule_meeting(event_title, start_time, end_time, attendees)
    print(f"Meeting scheduled successfully! Link: {link}")
    
# Call the method to schedule a meeting
auto_schedule_meeting()
