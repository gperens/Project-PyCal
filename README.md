# Project-PyCal
LTAT.03.001 course project to automate university calendar sync with Google Calendar

## Project description
Program can export users university calendar events from different sources and combine it to one schedule that is then automatically imported into Google Calendar.

### Functionality of the program
- Program is usable either from the GUI or CLI
- User can choose from 4 event sources: TalTech ÕIS, Tartu ÕIS, TalTech Moodle, Tartu Moodle
- Credentials are asked from the user for the relevant sources
- Event data is extracted from sources with HTTP requests, using the credentials to authenticate
- Google calendar access is gained by triggering OAuth sign-in dialog and Google Calendar API is used to write events into calendar

---

## Project rules
In this course, the project means a larger programming task on a topic chosen by yourself.

The best option is to use the project to create a program that helps you directly in your professional work or studies. But you can also choose a topic that reflects your personal interests, hobbies, etc. For example, the project could be related to some kind of human activity, such as answering customer queries, using a household appliance, playing a game, or so on. However, it should not be some well-known program found on the web.

The project has to make use of resources that are not taught in the core of our course. As an example, here are some interesting libraries that you can (but don't necessarily need to) use:

- pandas, numpy, matplotlib, sklearn – for data processing, visualization, and machine learning
- tkinter, easygui – for graphical user interfaces
- wit.ai – for speech recognition
- face_recognition – for facial recognition
- Python-sounddevice – for sound recording
- OpenCV – for image processing
- pygame – for creating games
- If you are unsure which topic you should select, please consult with the instructor!

The project must be done in pairs, and it is divided into three phases:

1. Form a pair and select a topic. In Moodle, please 1) register to a group together with your project partner; 2) submit a brief description of your project idea and goal. Due date: **April 1, 2022.**
2. Alpha version. By the end of this phase, submit an initial version of your program. Also, for the practice session, prepare a presentation where you describe the objectives, tools, implementation issues, and further plans related to your project.  **Due date: April 29, 2022.**
3. Beta version. By the end of this phase, complete all planned developments so that the project can be made available to the public. For the practice session, prepare a presentation where you describe what you did during this phase, describe your solution's strengths and limitations, and recap the lessons you learned from doing the project. **Due date: May 27, 2022.**

The size of the project can be estimated as follows. The total amount of work in the course is 6*26 = 156 hours. The project gives 24 points out of 100, so the amount of work for it is 24/100*156 = 37.44 hours per student. Since the project is done in pairs, the project's overall size is approximately 2*37.44 = 74.88 hours.

Your project will be graded according to the following criteria. To be graded, the program must be an original Python program. The size must minimally correspond to the estimated work hours of the project.

**1. General value.** The program should provide value to the user, i.e., yourself or others. It should allow the user to do something that is hard or impossible to do with other means.

**2. Usability.** The program should be easy to use and contain no errors, illogicalities, or unexpected surprises. Inputs and outputs should be clear and user-friendly. The code should be reasonably efficient.

**3. Readability.** The code needs to be readable to both you and a knowledgeable third party. It should be well organized and have a clear structure. This also includes proper use of whitespace and names of variables and functions.

**4. Documentation.** The code should be [well documented](https://realpython.com/documenting-python-code/). All functions and classes should have docstrings describing their purpose, arguments, functionality, etc. Places in the code that are harder to understand should be commented on.

For the alpha version, criteria 3 and 4 are more important. For the beta version, criteria 1 and 2 are more important.
In addition, you'll have an opportunity to present your project to others and give feedback to the other projects.

**5. Presentation of the project.** Your presentation should give an overview of your program and your work on it. The presentation should cover all essential aspects of the project.

**6. Feedback to other projects.** The feedback should be constructive and helpful for developing the project further.
