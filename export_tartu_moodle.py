import requests
import getpass
import json
import re
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Define export functions to authenticate with event source and get the events.
# All export functions should take user credentials as arguments and return the calendar events in iCal format.

def export_tartu_moodle():

    username = str(input("Enter your Tartu moodle username/email: "))
    # Use getpass module to collect user password without displaying the output on the screen
    password = getpass.getpass("Enter your Tartu Moodle password: ")

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
    payload = {"login": username,"passwd": password,"ctx": ctx,"flowToken": flow_token}
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
    payload = {"sesskey": sesskey,"_qf__core_calendar_export_form": "1","events[exportevents]": "all","period[timeperiod]": "custom","generateurl": "Hangi kalendri URL"}
    response = session.post(url, payload)
    soup = BeautifulSoup(response.text, "html.parser")
    ical_url = soup.find("div", {"class": "generalbox calendarurl"}).getText().split(" ")[2]

    response = requests.get(ical_url)
    if response.ok:
        print("")
        print("Tartu Moodle events exported successfully!")
        print("")
    cal = Calendar.from_ical(response.text)

    return cal