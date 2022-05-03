import requests
import getpass
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Define export functions to authenticate with event source and get the events.
# All export functions should take user credentials as arguments and return the calendar events in iCal format.

def export_tartu_ois():

    username = str(input("Enter your Tartu ÕIS username: "))
    # Use getpass module to collect user password without displaying the output on the screen
    password = getpass.getpass("Enter your Tartu ÕIS password: ")

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
        print("")
    cal = Calendar.from_ical(response.text)

    return cal