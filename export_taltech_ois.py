import requests
import re
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

# Defines export function to authenticate with event source and get the events.
# Export function should take user credentials as arguments and return the list
# of calendar events as dictionary objects in the format that Google Calendar expects.

def export_taltech_ois(username,password):
    
    session = requests.Session()

    url = "https://ois2.ttu.ee/uusois/!uus_ois2.ois_public.page?_page=9A46066693F9020547B19035E345EAEE"
    payload = {"p_mobiil": "big","p_mobiil_tel": "","p_type": "yld","p_user": username,"p_pwd": password}
    response = session.post(url, payload)
    
    url = "https://ois2.ttu.ee/uusois/!uus_ois2.ois_public.page?_page=21D02BFC64FA0CCC52A388D2A2990C7D90419DA7F185EAC0F686D0A892D49F92"
    response = session.get(url)
   
    ical_url = re.search("(null,')([\S]*?)(?=')", response.text).group(2)
    response = requests.get(ical_url)
    if response.ok:
        print("")
        print("Taltech ÕIS events exported successfully!")
    cal = Calendar.from_ical(response.text)
    
    # Currently part that turns calendar events into the format that Google Calendar expects is missing,
    # but similar logic could be used as in Tartu ÕIS exporter.