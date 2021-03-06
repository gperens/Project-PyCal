import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

# Original source for the authentication code is https://developers.google.com/calendar/api/quickstart/python

def google_auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # This credentials.json need to be generated from Google Cloud Platform,
            # see: https://developers.google.com/workspace/guides/create-credentials#oauth-client-id
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

# List existing calendars for user by names
def list_existing_cals():
    service = google_auth()
    calendar_list = service.calendarList().list().execute()
    names_list = []
    for calendar_list_entry in calendar_list['items']:
        names_list.append(calendar_list_entry['summary'])
    
    return names_list 

# Create a new calendar with provided name
def create_cal(cal_name):
    service = google_auth()
    new_cal_config = {'summary': cal_name, 'timeZone': 'Europe/Tallinn'}
    new_cal = service.calendars().insert(body=new_cal_config).execute()

# Get the calendar ID from its name 
def get_cal_by_name(name):
    service = google_auth()
    calendar_list = service.calendarList().list().execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary'] == name:
            cal_id = calendar_list_entry['id']
    
    return cal_id

# Delete a existing calendar by providing its name
def delete_cal_by_name(name):
    service = google_auth()
    cal_id = get_cal_by_name(name)
    service.calendars().delete(calendarId=cal_id).execute()

# Add the list of events into a calendar
def add_events(cal_name,events_list):
    service = google_auth()
    for event in events_list:
        imported_event = service.events().import_(calendarId=get_cal_by_name(cal_name), body=event).execute()
