import requests
import datetime
import json
import re
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Defines export function to authenticate with event source and get the events.
# Export function should take user credentials as arguments and return the list
# of calendar events as dictionary objects in the format that Google Calendar expects.

def export_tartu_moodle(email,password):

    session = requests.Session()

    # Perform series of back-and-forth requests, parse out different obscure token values from json and hidden input fields
    # because Tartu Moodle uses Microsoft authentication which is very messy.
    # I would not recommend anyone to try this with just Python requests unless you have a serious reverse engineering kink.


    # Request # 1
    url = "https://moodle.ut.ee/login/index.php"
    response = session.get(url)


    # Request # 2
    url = "https://moodle.ut.ee/auth/oidc/"
    response = session.get(url,allow_redirects=False)


    # Request # 3
    url = response.headers["Location"]
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    javascript_text = soup.find('script').get_text()
    config_json = json.loads(javascript_text[javascript_text.index('=')+1:-7])
    flow_token = config_json["sFT"]
    ctx = config_json["sCtx"]


    # Request # 4
    url = "https://login.microsoftonline.com/6d356317-0d04-4abc-b6b6-8c9773885bb0/login"
    payload = {"login": email,"passwd": password,"ctx": ctx,"flowToken": flow_token}
    response = session.post(url, payload)
    soup = BeautifulSoup(response.text, "html.parser")
    code = soup.find("input", {"name": "code"}).get("value")
    state = soup.find("input", {"name": "state"}).get("value")
    session_state = soup.find("input", {"name": "session_state"}).get("value")


    # Request # 5
    url = "https://moodle.ut.ee/auth/oidc/"
    payload = {"code": code,"state": state,"session_state": session_state}
    response = session.post(url, payload)
    # Now we are finally authenticated!!!


    # Request to get the session key for calendar export
    url = "https://moodle.ut.ee/calendar/export.php"
    response = session.get(url)
    # Use Regex to parse out session key
    sesskey = re.search('(sesskey":")([\S]*?)(?=")', response.text).group(2)


    # Requests to finally get the iCal link and then the file
    payload = {"sesskey": sesskey,"_qf__core_calendar_export_form": "1","events[exportevents]": "all","period[timeperiod]": "custom","generateurl": "Get calendar URL"}
    response = session.post(url, payload)
    soup = BeautifulSoup(response.text, "html.parser")
    ical_url = soup.find("div", {"class": "generalbox calendarurl"}).getText().split(" ")[2]

    response = requests.get(ical_url)
    if response.ok:
        print("")
        print("Tartu Moodle events exported successfully!")
    cal = Calendar.from_ical(response.text)

    
    # Reformat iCal events into the list of calendar events as dictionary objects in the format that Google Calendar expects.
    events_list = []

    for event in cal.walk():
        if event.name == "VEVENT":
            
            # Get subject code from category and prepend it to summary
            summary = event.get('categories').to_ical().decode() + " - " + event.get("summary").to_ical().decode()
            
            # Get the start and values for the event
            start = event.decoded("dtstart")
            end = event.decoded("dtstart")

            formated_event = {
                'iCalUID': event.get("uid").to_ical().decode(),
                'summary': summary,
                'description': event.get("description").to_ical().decode(),
                'start': {'dateTime': start.isoformat(), 'timeZone': 'Europe/Tallinn'},
                'end': {'dateTime': end.isoformat(), 'timeZone': 'Europe/Tallinn'}
            }

            events_list.append(formated_event)

    return events_list
