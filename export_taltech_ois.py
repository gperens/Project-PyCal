import requests
import getpass
import time
import json
import re
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

def export_taltech_ois():
    
    username = str(input("Enter your TalTech ÕIS username: "))
    password = getpass.getpass("Enter your TalTech ÕIS password: ")
    session = requests.Session()

    url = "https://ois2.ttu.ee/uusois/!uus_ois2.ois_public.page?_page=9A46066693F9020547B19035E345EAEE"
    payload = {"p_mobiil": "big","p_mobiil_tel": "","p_type": "yld","p_user": username,"p_pwd": password}
    response = session.post(url, payload)
    
    url = "https://ois2.ttu.ee/uusois/!uus_ois2.ois_public.page?_page=21D02BFC64FA0CCC52A388D2A2990C7D90419DA7F185EAC0F686D0A892D49F92"
    response = session.get(url)
   
    soup = BeautifulSoup(response.text, "html.parser")
    x = soup.find("input", {"name": "newsearch_button"}).get("value")
    y = re.search("(null,')([\S]*?)(?=')", response.text).group(2)
    response = requests.get(y)
    cal = Calendar.from_ical(response.text)
    print(cal)
