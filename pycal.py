import requests
import getpass
import time
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# If you get module_error then install the required packages with "pip install -r requirements.txt"

# Define different export functions to authenticate with event sources and export the calendar dates.
# All export functions should take user credentials as arguments and return the calendar events in iCal format.

def export_taltech_ois():
    # TODO
    # Problem with Taltech is there are no subjects for me this semester so I don't know how to test this.
    return None

def export_tartu_ois():

    username = str(input("Enter your Tartu ÕIS username: "))
    # Use getpass module to collect user password without displaying the output on the screen
    password = getpass.getpass("Enter your Tartu ÕIS password: ")

    session = requests.Session()

    # Perform series of back-and-forth requests because Tartu ÕIS uses SAML authentication which is messy.
    url = "https://ois2.ut.ee/api/user/sso?clientType=student"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    auth_sate = soup.find("input", {"name": "AuthState"}).get("value")

    url = "https://auth.ut.ee/idp/module.php/core/loginuserpass.php"
    payload = {"username": username,"password": password, "AuthState": auth_sate}
    response = session.post(url, payload)
    soup = BeautifulSoup(response.text, "html.parser")
    saml_response = soup.find("input", {"name": "SAMLResponse"}).get("value")
    relay_state = soup.find("input", {"name": "RelayState"}).get("value")

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
        print("")
    cal = Calendar.from_ical(response.text)

    return cal

def export_taltech_moodle():
    # TODO
    return None

def export_tartu_moodle():
    # TODO
    return None


# Greet user and explain what this program does and what do they need to do next.

print("""
Hello and welcome to PyCal!
This program exports all your school calendar events from different sources and imports them into your Google Calendar.

To start, you have to choose the sources from where you wish to export events.
Possible options are:
1. TalTech ÕIS
2. Tartu ÕIS
3. TalTech Moodle
4. Tartu Moodle

Enter all the numbers for sources you wish to include. E.g. Entering "14" will export from TalTech ÕIS and Tartu Moodle.
""")
sources = str(input("Enter your choices: "))

# Call the source functions depending on the user choice and add them into the list of calendars
calendars = []
if "1" in sources:
    calendars.append(export_taltech_ois())
if "2" in sources:
    calendars.append(export_tartu_ois())
if "3" in sources:
    calendars.append(export_taltech_moodle())
if "4" in sources:
    calendars.append(export_tartu_moodle())


# Demo section for alpha just printing out the calendar events for selected source:
def demo_print(cal):
    for event in cal.walk():
        if event.name == "VEVENT":
            if event.name == "VEVENT":
                print("Event name: ",event.get("summary"))
                print("Teacher: ",event.get("description"))
                print("Location: ",event.get("location"))
                print("Star time: ",event.decoded("dtstart"))
                # print("End time: ",event.decoded("dtend"))


# Do the demo_print for calendars that were imported
for i in calendars:
    time.sleep(3)
    demo_print(i)


# TODO - Combine calendar data from different sources.

# TODO - Trigger OAuth flow to gain access to Google Calendar API

# TODO - Write calendar data into Google Calendar using the API

# TODO - Print out success message if everything went well or error message on what went wrong.
