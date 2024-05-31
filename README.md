

# https://developers.google.com/sheets/api/quickstart/python

# ***LovinPlans***: The Ultimate Task Management Tool!
## A TODO List Python CLI 

### **Table of content:**
- [Overview](#overview)
- [Target audience](#item-two)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Additional testing](#additional-testing)
- [Known bugs and issues](#known-bugs-and-issues)
- [Possible improvements](#possible-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)


## Overview
This application was developed as part of Milestone Project 3 for the Diploma in Full Stack Software Development program at Code Institute.

The main purpose of this project is to build an interactive command line application utilizing the Python programming language.

The result of the project is the ***LovinPlans*** command line interface (CLI) application that allows the user to dynamically create and edit a simple TODO list, and to follow-up the tasks as they are being executed. 

***LovinPlans*** is a user-friendly CLI app that demonstrates how to create, edit, and track tasks effortlessly with the purpose to help the users to stay focused and productive. Nevertheless, the app is not a fully developed product, but rather a proof of acquired Python programming skills compatible to the Milestone Project 3 requirements.

## Application development 
This Python CLI application has been developed iteratively, following basic Agile development principles. 
While still in the learning phase of Agile methodologies, I mostly focused on implementing a small number of user stories per iteration. 
Below are examples of some of the user stories that guided the development process:
- As a potential user, I need to register and to set up a user profile.
- As a registered user, I want to be able to delete my acount.
- As a user, I want to clean up the console before I access another user menu option.
- As a user, I want to see clearly the overdue tasks.

The progress was nonlinear, with many bugs that occured and quite painful code refactoring to adhere to the DRY (Don't Repeat Yourself) principles.  

A Lucid wireframe was used to guide the high-level the app development during the iterations. The wireframe has been  
![App flowchart](/assets/images/Flowchart_CLI_TODO.png)
*LovinPlans Lucid flowchart.*


## Target audience
Theoretically, the the ***LovinPlans*** app is designed to cater to a diverse range of users seeking a simple yet powerful task management solution. These user stories helped shape the functionality and usability of our CLI application, ensuring it meets the needs of its users effectively
The target audience for the app includes tech-savvy, goal-oriented, and organized individuals who prioritize personal productivity. Furthermore, the app is designed to be inclusive, aiming to accommodate users from diverse geographic regions, cultures, and backgrounds worldwide.

## Features
A quick demonstration of using the app can be found here: 
- For the main menu options: [***here.***](assets/images/Demo-functionality.gif)
- For the user menu options: [***here.***](assets/images/Demo-functionality.gif)

### **1. User-friendly interface**
***LovinPlans*** is a CLI application that provides an intutive inteface through console dialogs.   

The app opens with the Main Menu than provides the following options: 
- 1 : User Login
- 2 : Register a new user
- 3 : Show the help content for running the application
- 4 : Exit the application

The app doesn not require a steep learning curve to start using it, in order to faciliate the usage, it comes with a Help Menu that for the first time users.
 
- In order to facilitate beyond the 24 rows provided in the Heroku terminal, the user is provided with functionality to presiodically clean up the console outputs. 
In this way, the user can stay logged and explore the app functionality without constraints related to the terminal height. 
- The app allows the user to switch betwwen menu options without exiting the application.
- Closing the application is possible throught the menu options, as well as through forced exit         
- The console printing is ituitive yet simple, using a tabel formatting style for displaying the worksheet information.   

### **2. Create and delete user accounts**

### **3. Task Creation and Editing**
- Users can effortlessly create new tasks and edit existing ones with just a few clicks. 

### Help Menu 
The Help Menu was printed using the user_help() function that opens and writes a Markdown file in the console, as described at  
[https://rich.readthedocs.io/en/stable/](https://rich.readthedocs.io/en/stable/console.html).


### **3. Task follow up**
- The app allows users to enter task details such as the due date.   
- At login, the due date of each user task is checked against the curent date. 
- If a task has passed its due date, the task status changes from 'active' to 'overdue', and the overdue tasks are 
also marked with light red color background in the worksheet.
 
### **4. Cross-Platform Accessibility**
- The app can be used on any device (mobile, tablet, laptop/desktop) that is connected to internet.  
 More details about the app functionality are provided in the [Usage and screenshots](#usage-and-screenshots) section.


## Technologies Used
The app was build using Python 3.11.7 version. 
usning an external VSCode IDE. Windows 11 desktop. 

The script utilizes a functional design approach that (***hopefully***) adheres to the DRY (Don't Repeat Yourself) principles.

The structure of the app is provided in the [run.py file](run.py) that containts the Python script. 


### Python call stack
The script contains the following main sections:
- External modules imports
- Connection to Google Sheets via API calls using private credentials.  
- Declaration of constant variables such as:
    - connections to the project LovePlanning Google Sheet
    - the names of the Google worksheets used by the app
    - the column names (headers) of those worksheets
    - standard user choices available through the console 
- Python function definitions with a main() function that calls the stack.
    - As a rule of thumb, All functions that receive more than two arguments are called using keyword arguments.
    - To the best of my Python abilities, I tried to use type hints for all function arguments. 


#### Python modules
The application uses the following external Python modules:  
- gspread 6.1.0 ([Python API for Google Sheets](https://docs.gspread.org/en/v6.0.0/))
- gspread_formatting 1.1.2 ([Complete Google Sheets formatting support for gspread worksheets](https://pypi.org/project/gspread-formatting/))
- google-auth 2.29.0 ([Google Auth Library for Python](https://google-auth.readthedocs.io/en/master/))
- google-auth-oauthlib 1.2.0 ([Google Authentication Library](https://pypi.org/project/google-auth-oauthlib/))
- regex 2024.5.10 ([Alternative regular expression module, to replace re.](https://pypi.org/project/regex/))
- rich 13.7.1 ([Python library for writing rich text](https://rich.readthedocs.io/en/stable/introduction.html))
- tabulate 0.9.0 ([Pretty-print tabular data](https://pypi.org/project/tabulate/))

The extrenal modules were installed locally via `pip install` command in the VSCode PowerShell. 

### Local Development and deployment
The application developement was done using the VSCode IDE version 1.89.1. with the [Microsoft Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed.

The app can be run locally using the `python run.py` command in the terminal.


### Markdown 
The Markdown formatting for README.md and HELP.md files was done according to the documentation provided at
[www.markdownguide.org](https://www.markdownguide.org/basic-syntax/). 


### Cloud deployment
The app is currently deployed on [Heroku Cloud Application Platform](https://www.heroku.com)
For cloud deployment, the [dependency requirements file](requirements.txt) was compiled using the \
`pip freeze > requirements.txt` command in the VSCode PowerShell.

The app is currently deployed on github and can be accessed at: https://love-planning-cli-f243068a58dc.herokuapp.com/. 


### Testing

#### Additional tools and services
- The [***favicon***](/assets/favicon/favicon.ico) for the website was generated from text using the [favicon.io](https://favicon.io/) tools.
- All the other icons were obtained from [fontawesome.com](https://fontawesome.com/) website.
- The use of ChatGPT was restrictes to getting sensible inputs for the text content in the website and for proof-checking the language.

### Responsive design
- The app uses responsive design principles such media queries and flexible layouts to ensure proper interaction across various devices and screen sizes. 
- The app interface adapts dynamically based on the device's viewport size, providing a seamless and consistent user experience on desktops/laptops, tablets, or smartphones.

### Accessibility
- Aria-labels for screen readers were included in the sections, input and button HTML elements of the app to ensure semantic elements and enhance accessibility. This approach helps improve the semantic understanding of the content and ensures that the web page becomes easy to navigate and to be understood by all users, especially those using screen readers. 

## Usage and screenshots
###  **1. Creating a Task**
#### To create a new task, click on the "Add Task" button or the plus icon located at the top or bottom of the task list.
#### Enter the task description in the text input field. 

![Add task dialig box](/assets/images/task1.webp "Add task: opening the dialog box")

#### Select an activity (personal activity, work-related or errands).
![Select activity dialig box](/assets/images/task2.webp "Add task: select activity")

#### Select the task priority (urgent/chore).
![Select task relevance dialig box](/assets/images/task3.webp "Add task: select task relevance")

#### Once you've filled out the task details, click the "OK" button to add the task to your list.
#### The task entry contains:
- A task name field that can be edited on click action.
- Edit butoon on the left side  
- A Bin Trash icon on the right side
- The selected task attributes are below the task name, on the left and the right side respectivelly.
- When a task is entered, the task tracking field updates the counters by task activities and categories.
- Error checks are placed to prevent submitting an invalid text entry (3-40 characters required for a valid task name)
    or ill formatted task (missing attributes).

![Add task to the Todo list](/assets/images/task4.webp "Add new task to the list")

### **2. Editing a Task**
- By clicking on the task name enables a prompt window for editing the text. 
- The new text input is validated before utpading the task name 

![Add task to the Todo list](/assets/images/task5.webp "Add new task to the list")

### **3. Complete/reactivate tasks**
- A left click on the edit button (lef side) opens a confirmation window 
- For OK selection, the task name is striked and font size reduces, while the edit button is checked.
    - The task tracking *decrements* the scores for active tasks
    - If all task are completed, the message "All Task Completed" marks the event.
- Note that pressing the Cancel button on the task completion confirmation window will delete the task  

![Add task to the Todo list](/assets/images/task6.webp "Add new task to the list")

- To reactivate a task, click on the edit button and press the OK button on the confirmation window.
    - The task name and edit button are restored to previous styling
    - The task tracking *increments* the scores for active tasks

![Add task to the Todo list](/assets/images/task7.webp "Add new task to the list")


### **4. Deleting a task**
Removing a task from the list can be done in two ways: 
- Clicking on the Bin Trash icon opens a confirmation window. 
    - Press OK to permanently remove the task from the list 
#### or 
- Press the Cancel button on the task completion from the confirmation window  (see [Complete/reactivate tasks](#3.-complete/reactivate-tasks) section)

![Add task to the Todo list](/assets/images/task8.webp "Add new task to the list")


### **5.Tracking the task list**
- When a task is marked as completed and/or removed from the list, the task tracking field updates the counters by task activities and categories.
- If all task are completed, the message "All Task Completed" marks the event.

## Additional testing

### Devices and browsers
Additional testing was performed on my private devices Windows 11 devices (desktop and laptop), as well as
on my smartphone (Samsung Galaxy S21) operating on Android OS, using the following web browsers: 
- Google Chrome: Version 123.0.6312.124
- Brave: version 1.65.114 Chromium: 124.0.6367.60 (Official Build) (64-bit)
- Microsoft Edge: Version 124.0.2478.51 (Official build) (64-bit)

### Tested features:
- 

- add new tasks (*pass*)
    - text editing and error checking for min/max text length
    - task activity selection (one at the time)
- text editing for an existing task (*pass*)
    - update the text in the task card
    - check for min/max text length  
- incrementing the task tracking score when adding a new task (*pass*)
    - incrementing the task tracking score when reactivating a previously completed task
    - decrementing the task tracking score
- mark a task as completed (*pass*)
    - editing tool action (press OK button on the 'Is the task completed?' prompt window )
    - bin trash icon action (press OK button on the prompt window)
- remove a task (*pass*)
    - editing tool action after task copletion confirmation (press OK button on the 'Remove task?' prompt window)
    - using the bin trash icon action (press OK button on the prompt window)
- responsiveness on various screen sizes (*pass*)   

## Known bugs and issues
- The text input is not restored after the error checking is run: the app behaviour is to reset all the inputs such that the user starts with a clean dialog window.   
- The browser specific promt windows triggered by the error checks doesn't contain a No-button (but the Cancel button has the same role): creating custom promt windows would improve the overall user experience.  
- There is a unfortunate typo in the name of the respository ('Portololoio' instead of 'Portofolio') that has to be fixed.

## Possible improvements
### Functionality for user accounts and data storage. 
In its current state, the app can only be user not provide storage for the task list and tracking data. The consequence is that each time the page is refreshed, all the information is gone. 
It would be nice to include user account and database connections such that the information is stored permanatly and the users can login in their accounts.
### Filtering and Sorting Tasks
- Filter and sort options to organize and view the tasks according to specific criteria.
- Possible filters: 
    - task status (e.g., active or ccompleted tasks)
    - activity type (work, leisure, etc)
    - task relevance/importance (urgent, chore) by due date or incoming within a certain time horizon.
### Reminders
- Set due dates with automatic reminder to receive timely notifications for upcoming tasks and deadlines.
- Day-time picker
- Check for task overlapp and possible collisions
### Dialog windows/menus
- Replace the prompt windows in the browsers with custom forms. For instance, it would a better user experience to replace the 'Cancel' button in the promt windows that pop-up during task editing and handling with a 'No' button.
- Add intercativity to all task features, including re-catogorizing and re-styling the theme (dark/light) and the button colors. 
### Collaboration tools
- Include features for inviting people to participate in various tasks, sharing task lists and/or assigning tasks to team members.
- Add the tools to allow the collaborators would have access to view, edit, and comment on the tasks.

## Contributing
### To contribute to the ***LovinPlans*** project:
- Fork the repository on GitHub to create your own copy.
- Clone the forked repository to your local machine.
- Make your desired changes, whether it's fixing a bug, adding a feature, or updating documentation.
- Commit your changes with clear messages.
- Push your commits to your forked repository on GitHub.
- Submit a pull request detailing your changes and their benefits.

## License
### Open Source
As an open-source project, ***LovinPlans*** encourages transparency, and community involvement. 
The code of the app is available on GitHub, such that developers can view, fork, and contribute to the project if they wish so.

## Acknowledgements
The code for setting callbacks to handle the events for task activities and relevance buttons was adapted from the *Stack Overflow* post available at: 

https://stackoverflow.com/questions/71346490/how-do-i-make-only-one-button-can-be-selected-at-time