import requests
import datetime
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Defines export function to authenticate with event source and get the events.
# Export function should take user credentials as arguments and return the list
# of calendar events as dictionary objects in the format that Google Calendar expects.

def export_tartu_ois(email,password):

    username = email.split("@")[0]

    session = requests.Session()

    # Perform series of back-and-forth requests because Tartu ÕIS uses SAML authentication which is messy.

    # Request # 1    
    url = "https://ois2.ut.ee/api/user/sso?clientType=student"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    auth_sate = soup.find("input", {"name": "AuthState"}).get("value")

    # Request # 2
    url = "https://auth.ut.ee/idp/module.php/core/loginuserpass.php"
    payload = {"username": username,"password": password, "AuthState": auth_sate}
    response = session.post(url, payload)
    soup = BeautifulSoup(response.text, "html.parser")
    saml_response = soup.find("input", {"name": "SAMLResponse"}).get("value")
    relay_state = soup.find("input", {"name": "RelayState"}).get("value")

    # Request # 3
    url = "https://ois2.ut.ee/Shibboleth.sso/SAML2/POST"
    payload = {"SAMLResponse": saml_response, "RelayState": relay_state}
    response = session.post(url, payload)
    # Finally we received JWT token as a cookie which helps us to authenticate all other requests we wish to make.
    jwt = session.cookies.get_dict()["jwt"]

    # This request provides us with unique link to our semester calendar iCal file
    url = "https://ois2.ut.ee/api/timetable/personal/link/en"
    response = session.get(url, headers={"Authorization": f"Bearer {jwt}"})
    # Save iCal file URL
    ical_url= response.text[1:-1]

    # Request the iCal file and save it as a iCal object
    response = requests.get(ical_url)
    if response.ok:
        print("")
        print("Tartu ÕIS events exported successfully!")
    cal = Calendar.from_ical(response.text)

    
    # Reformat iCal events into the list of calendar events as dictionary objects in the format that Google Calendar expects.
    events_list = []

    for event in cal.walk():
        if event.name == "VEVENT":
            
            # Get category and description values if they exist and put them together as description
            description = ""
            if event.get('categories') is not None:
                description += event.get('categories').to_ical().decode().title() + "\n"
            if event.get("description") is not None:
                description += event.get("description").to_ical().decode() + "\n"
            # Get location value if it exists
            location = ""
            if event.get("location") is not None:
                location = event.get("location")
            # Get exeption dates if they exist
            exdate = ""
            if event.get("exdate") is not None:
                exdate = "EXDATE:" + event.get("exdate").to_ical().decode()
            
            # Get the start value for the first recurring event
            start = event.decoded("dtstart")
            # Get the end value for the first recurring event by adding duration to the start value
            end = start + event.decoded("duration")
            # Get the recurrance rule
            rrule = "RRULE:" + event.get("rrule").to_ical().decode()

            formated_event = {
                'iCalUID': event.get("uid").to_ical().decode(),
                'summary': event.get("summary").to_ical().decode(),
                'description': description,
                'location': location,
                'start': {'dateTime': start.isoformat(), 'timeZone': 'Europe/Tallinn'},
                'end': {'dateTime': end.isoformat(), 'timeZone': 'Europe/Tallinn'},
                'recurrence': [rrule,exdate]
            }

            events_list.append(formated_event)

    return events_list