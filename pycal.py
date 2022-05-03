from icalendar import Calendar, Event
from export_tartu_ois import export_tartu_ois
from export_tartu_moodle import export_tartu_moodle
from export_taltech_ois import export_taltech_ois
from export_taltech_moodle import export_taltech_moodle

# If you get module_error then install the required packages with "pip install -r requirements.txt"

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
