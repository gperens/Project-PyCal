
###  High-level pseudocode program structure: ###

# Greet user and explain what this program does and what do they need to use it

print("Hello and welcome to PyCal!")

# Ask user which event source(s) they want to use. Options:
# - TalTech ÕIS
# - Tartu ÕIS
# - TalTech Moodle
# - Tartu Moodle

# Define different functions to authenticate with event sources:

def auth_ut_moodle():
    return None

def auth_ttu_moodle():
    return None

def auth_ut_ois():
    return None

def auth_ttu_ois():
    return None

# Depending on the choice of event sources call different auth functions
# and save the necessary credentials.

# Trigger OAuth flow to gain access to Google Calendar API

# Define different functions per event source to request for calendar data

# Save calendar data in variable and modify it into suitable format

# Combine calendar data from different sources.

# Write calendar data into Google Calendar using the API
# - We can ask if user wants to create a new calendar or write into an
#   existing one

# Print out success message if everything went well or error message on what went wrong.




