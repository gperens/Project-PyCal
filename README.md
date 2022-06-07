# Project-PyCal
LTAT.03.001 course project to automate university calendar sync with Google Calendar

## Project description
Program can export users university calendar events from different sources and combine it to one schedule that is then automatically imported into Google Calendar.

### Current functionality of the program
- Program is usable from CLI
- User can choose from 2 event sources: Tartu ÕIS and Tartu Moodle
- Credentials are asked from the user for the relevant sources
- Event data is extracted from sources with HTTP requests, using the credentials to authenticate
- Google calendar access is gained by triggering OAuth sign-in dialog and Google Calendar API is used to write events into calendar

### Planned functionality of the program
- Program will have a simple GUI (possibly with Tkinter)
- TalTech ÕIS and TalTech Moodle will be added as event sources
- Avoid the need for users to set up their own Google Cloud project to get API keys
- Some type of automated scheduling which will run the calendar update at some interval

---

## How to set up and use PyCal

1. Clone this repo to your local machine
2. Follow this instruction https://developers.google.com/workspace/guides/create-credentials#oauth-client-id to create
   Google Cloud project and generate an OAuth client ID credentials for Desktop App. This is needed for Google Calendar access.
3. From the last step you should be able to download `credentials.json` file, move that into the project folder.
4. Run `pycal.py` file and complete the OAuth flow which will generate a `token.json` into your project folder (this is only needed once).
5. After that, follow the instruction of the program and everything should work.  