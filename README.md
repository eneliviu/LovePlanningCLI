
# ***<center><font color="red"> LovinPlans</font>***: The Ultimate Task Management Tool!</center>
## <center> A TODO List Python CLI </center>

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
- [Documentation version](#Documentation-version)


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

During iterations, the overview over the app development was guided using Lucid wireframes like the one shwon below:

![App flowchart](/assets/images/Flowchart_CLI_TODO.png)<br>
<center>*LovinPlans: Lucid flowchart for application development.*</center><br> 

## Target audience
Theoretically, the the ***LovinPlans*** app is designed to cater to a diverse range of users seeking a simple yet powerful task management solution. These user stories helped shape the functionality and usability of our CLI application, ensuring it meets the needs of its users effectively.

The target audience for the app includes tech-savvy, goal-oriented, and organized individuals who prioritize personal productivity. Furthermore, the app is designed to be inclusive, aiming to accommodate users from diverse geographic regions, cultures, and backgrounds worldwide.

## Features

A quick demonstration of using the app can be found here: 

- For the main menu options: [***here.***](assets/images/Demo-functionality.gif)

- For the user menu options: [***here.***](assets/images/Demo-functionality.gif)


### **1. A user-friendly interface**

***LovinPlans*** is a CLI application that provides an intuitive usage experience through console dialogs.   

- The app opens with a Main Menu than provides the following options: 
    - 1 (User Login): Login of regsitered users via username and password;
    - 2 (Register a new user): Requires a vlaid username, password and email address to creates a user profile 
        and a dedicated user worksheet for storing the tasks;
    - 3 (Help): Show the help menu content for running the application;
    - 4 (Exit): Gracefully exiting the application.

![Main menu](/assets/images/main-menu.png#center)
*<center><font color="red">LovinPlans</font>: App initialization and main menu configuration*.</center><br> 

- After the Login, the User Menu section handles the following options for the registered users:
    - 1 (View tasks): List all tasks;
    - 2 (Add task): Add a new task; 
    - 3 (Delete task): Delete a task;
    - 4 (Delete account): Delete user account;
    - 5 (Exit): Return to the main menu.

![User menu](/assets/images/user-menu.png) <br>
*<font color="red">LovinPlans</font>: User menu configuration.*<br> 

- In addition, the users can invoque forced exit by entering 'exit' from the keyboard instead of the suggested options. In the script,  
the forced exit calls the sys.exit(0) Python routine to close the app gracefully.
- The app is user-friendly and easy to start using without a steep learning curve. To assist new users, the Main Menu includes a Help Menu option that offers a quick tour of the app's functionality (more details in the [Help Menu](#help-menu) section).
- A great deal of attention was put on handling exceptions in order to provide a positive UX. The exception handling was implemented using try-except blocks for detect error during executions and provide relevant error messages to the user. 
- To facilitate working beyond the 24 rows provided in the Heroku terminal, the app offers functionality for periodically cleaning up console outputs. 
This allows the user to stay logged in and explore the app's functionality without being constrained by the terminal height.
- The app allows users to switch between menu options without exiting the application using recursive function calls.
- The console printing is intuitive yet simple, utilizing a table formatting style for displaying worksheet information.

### **2. Use of Google Sheets**

The user information and the TODO lists are stored in a dedicated document hosted by Google Sheets. 
The app uses two categories of worksheets: 
- users-worksheet for storing the user login information and contact details such as:
    - user id
    - username
    - email address
    - user password
    - number of tasks

![users worksheet](/assets/images/users-worksheet.png) <br>
*<font color="red">LovinPlans</font>: The 'users' worksheet containing the registered users profiles.*<br> 

- provate user worksheets for storing the user login information and contact details such as:
    - task id
    - task description
    - task creation date (MM-DD-YYYY format)
    - task due date (MM-DD-YYYY format)
    - status (active / overdue)
By convention, the registered usernames are used for labeling the dedicated user worksheets. 

![user worksheet](/assets/images/user-worksheet.png) <br>
*<font color="red">LovinPlans</font>: A typical user worksheet containing the users tasks.*<br> 

### **3. Create and delete user accounts**
- New users can easily register and create their own TODO list with a few inputs.
- User registration requires:
    - a valid username (non-empty)
    - a password  of at minimum eight chatacters, of which at least one capital letter and two numerals (e.g., Password12)
    - an email address with valid formatting (e.g., someone@somewhere.com) that passess the regex
    -  

### **4. Task Creation and Editing**
- Users can effortlessly create new tasks and edit existing ones with just a few clicks. 
- The process of creating a new task requires:
    - a (non-empty) text input of maximum 44 characters
    - a due date specification using the MM-DD-YYYY formatting (e.g., 12-30-2024)
- By default, all newly created tasks receive an 'active' status 
- The current local time is also registered in the user worksheet to allow tracking of the overdue tasks. 

### **5 Task Views**
- The user tasks are printed on the terminal using the tabulate Python module that allows formatting the output as a table.
- The task viewing functionality is also available for listing the available tasks before selecting the ones to be removed.    

![Tasks view](/assets/images/tasks-view.png) <br>
*<font color="red">LovinPlans</font>: Printing the user tasks on the Herou console.*<br> 

### **Clear the terminal option**
- After each main operation such views or multiple entries during user registation or task deletion, the app provides the option to clear the
terminal to eliminate the cluttering provide a positive UX to the user.

![Clear terminal](/assets/images/clear.png) <br>
*<font color="red">LovinPlans</font>: Option to clear the terminal.*<br> 



### **Help Menu** 
- The Help Menu provides a quick overview of the main app functionality.
- The Help Menu content was printed using the user_help() function that opens and writes a Markdown file in the console, as described at  
[https://rich.readthedocs.io/en/stable/](https://rich.readthedocs.io/en/stable/console.html).

![Help menu](/assets/images/help-menu.png)<br>
*<font color="red">LovinPlans</font>: Help menu content.*<br> 

### **3. Task follow up**
- The app allows users to enter task details such as the due date.   
- At login, the due date of each user task is checked against the curent date. 
- If a task has passed its due date, the task status changes from 'active' to 'overdue', and the overdue tasks are 
also marked with light red color background in the worksheet.
 
### **4. Cross-Platform Accessibility**
- The app can be used on any device (mobile, tablet, laptop/desktop) that is connected to internet.  
 More details about the app functionality are provided in the [Usage and screenshots](#usage-and-screenshots) section.


## Technologies Used
The app was written in Python 3.11.7 version using an external VSCode IDE on a Windows 11 desktop. The script utilizes a functional design approach that (***hopefully***) adheres to the DRY (Don't Repeat Yourself) principles. The structure of the app is provided in the [run.py file](run.py) that containts the Python script. 

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
    - As a rule of thumb, all functions that receive more than two arguments are called using **kwargs.
    - Docstrins were placed after function definitions to document the code.
    - Where necessary, text comments were placed in the script to provide further explanations. 
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

## Usage and screenshots

###  **1. Creating a Task**
#### To create a new task, click on the "Add Task" button or the plus icon located at the top or bottom of the task list.
#### Enter the task description in the text input field. 


#### Select an activity (personal activity, work-related or errands).

#### Select the task priority (urgent/chore).

#### Once you've filled out the task details, click the "OK" button to add the task to your list.
#### The task entry contains:
- A task name field that can be edited on click action.
- Edit butoon on the left side  
- A Bin Trash icon on the right side
- The selected task attributes are below the task name, on the left and the right side respectivelly.
- When a task is entered, the task tracking field updates the counters by task activities and categories.
- Error checks are placed to prevent submitting an invalid text entry (3-40 characters required for a valid task name)
    or ill formatted task (missing attributes).


### **2. Editing a Task**
- By clicking on the task name enables a prompt window for editing the text. 
- The new text input is validated before utpading the task name 

### **3. Complete/reactivate tasks**
- A left click on the edit button (lef side) opens a confirmation window 
- For OK selection, the task name is striked and font size reduces, while the edit button is checked.
    - The task tracking *decrements* the scores for active tasks
    - If all task are completed, the message "All Task Completed" marks the event.
- Note that pressing the Cancel button on the task completion confirmation window will delete the task  

- To reactivate a task, click on the edit button and press the OK button on the confirmation window.
    - The task name and edit button are restored to previous styling
    - The task tracking *increments* the scores for active tasks


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

***HERE***

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

## <font color="red">Known bugs and issues</font>
- Switching back to the Main Menu from the User Menu not implemented yet;
- In rare situations, the app may exit ungracewfully due to API call errors, which were not thorougly tested.

If you encounter issues or bugs, please create an issue by clicking [here](https://github.com/eneliviu/LovePlanningCLI/issues).

## Possible improvements

### Improved task editing
- Task categories could be introduced such that the users can categorize their tasks by importance (e.g., urgent, chore)
and/or type categories (e.g., work, personal, etc). 
- Functionality for re-catogorizing and editing existing tasks.

### Filtering and Sorting Tasks
- Filter and sort options to organize and view the tasks according to specific criteria.
- Possible filters: 
    - task status (e.g., active, completed or overdue tasks)
    - activity type (work, personal, etc)
    - task relevance/importance (urgent, chores) by due date or incoming within a certain time horizon.

### Reminders
- Set due dates with automatic reminder to receive timely notifications for upcoming tasks and deadlines.
- Add a day-time picker to improve the UX
- Check for task overlapp and possible collisions


### About menu option
For further development, including an About option would to provide more information about the various releases and other information
that helps keeping the users updated.  

### Collaboration tools
- Include features for inviting people to participate in various tasks, sharing task lists and/or assigning tasks to team members.
- Add the tools to allow the collaborators would have access to view, edit, and comment on the tasks.

Some of the improvements mentioned in this section (such as the task classification or an About menu option) were not introduced in the current release due to  the printing space limitations imposed in the Heroku terminal.

## Contributing
### To contribute to the ***LovinPlans*** project:
- Fork the repository on GitHub to create your own copy.
- Clone the forked repository to your local machine.
- To fork the project:
    - Click the "Fork" button on the top-right corner of the repository page 
    - Clone Your Fork by running the following command in the terminal or command prompt: 
        `git clone https://github.com/your-username/repository-name.git`
- Make your desired changes, whether it's fixing a bug, adding a feature, or updating documentation.
- Commit your changes with clear messages.
- Push your commits to your forked repository on GitHub.
- Submit a pull request detailing your changes and their benefits.

## License
### Open Source
As an open-source project, ***LovinPlans*** encourages transparency, and community involvement. 

The code is available on GitHub, such that developers can view, fork, and contribute to the project if they wish so.

## Acknowledgements
- Further details on the usage of Google Sheets API were obtained from https://developers.google.com/sheets/api/quickstart/python
- Printing the Markdown file in the console used for the Help-menu followed the expamples provided at https://rich.readthedocs.io/en/stable/console.html
- Formatting the worksheet cell background color followed the examples from https://gspread-formatting.readthedocs.io/en/latest/#
- The use of ChatGPT was restricted to getting sensible inputs for the text content in the Readme-file and for proof-checking the language.

## Documentation version
Last update May 31st, 2024