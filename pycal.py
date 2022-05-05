import getpass
from icalendar import Calendar, Event
from export_tartu_ois import export_tartu_ois
from export_tartu_moodle import export_tartu_moodle
from export_taltech_ois import export_taltech_ois
from export_taltech_moodle import export_taltech_moodle

# If you get module_error then install the required packages with "pip install -r requirements.txt"


# General function to gather university login credentials
def creds_uni(uni_name):
    # Email value can be used directly as an username for Moodle. For ÕIS, we need to use the part before @ttu.ee/@ut.ee
    email = str(input(f"Enter your {uni_name} Uni-ID email address: "))
    # Use getpass module to collect user password without displaying the output on the screen
    password = getpass.getpass(f"Enter your {uni_name} Uni-ID password: ")

    return email, password


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

# Gather necessary credentials and call the right source functions depending on the user choice and add them into the list of calendars
# This is implemented in a way that we don't ask credentials twice for the same university

calendars = []
if "1" in sources:
    taltech_creds = creds_uni("TalTech")
    calendars.append(export_taltech_ois(taltech_creds[0],taltech_creds[1]))
if "2" in sources:
    tartu_creds = creds_uni("Tartu")
    calendars.append(export_tartu_ois(tartu_creds[0],tartu_creds[1]))
if "3" in sources:
    try:
        calendars.append(export_taltech_moodle(taltech_creds[0],taltech_creds[1]))
    except:
        taltech_creds = creds_uni("TalTech")
        calendars.append(export_taltech_moodle(taltech_creds[0],taltech_creds[1]))
if "4" in sources:
    try:
        calendars.append(export_tartu_moodle(tartu_creds[0],tartu_creds[1]))
    except:
        tartu_creds = creds_uni("Tartu")
        calendars.append(export_tartu_moodle(tartu_creds[0],tartu_creds[1]))


# Demo section for alpha just printing out the calendar events for selected source:
def demo_print(cal):
    for event in cal.walk():
        if event.name == "VEVENT":
            print("Event name: ",event.get("summary"))
            print("Teacher: ",event.get("description"))
            print("Location: ",event.get("location"))
            print("Star time: ",event.decoded("dtstart"))
            # print("End time: ",event.decoded("dtend"))


# Do the demo_print for calendars that were imported
for i in calendars:
    demo_print(i)


# TODO - Combine calendar data from different sources.

# TODO - Trigger OAuth flow to gain access to Google Calendar API

# TODO - Write calendar data into Google Calendar using the API

# TODO - Print out success message if everything went well or error message on what went wrong.
