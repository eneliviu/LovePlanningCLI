
# ***<center><font color="red"> LovinPlans</font>***: The Ultimate Task Management Tool!</center>
## <center> A TODO List Python CLI </center>

### **Table of content:**
- [Overview](#overview)
- [Application development](#application-development)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Manual testing](#manual-testing)
- [Known bugs and issues](#known-bugs-and-issues)
- [Possible improvements](#possible-improvements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Documentation version](#documentation-version)


## Overview
This application was developed as part of Milestone Project 3 for the Diploma in Full Stack Software Development program at Code Institute.

The main purpose of this project is to build an interactive command line application utilizing the Python programming language.

The result of the project is the ***LovinPlans*** command line interface (CLI) application that allows the user to dynamically  
create and edit a simple TODO list, and to follow-up the tasks as they are being executed.

***LovinPlans*** is a user-friendly CLI app that demonstrates how to create, edit, and track tasks effortlessly with the purpose  
to help the users to stay focused and productive. Nevertheless, the app is not a fully developed product, but rather a proof of acquired  
Python programming skills compatible to the Milestone Project 3 requirements.

### Target audience
Theoretically, the the ***LovinPlans*** app is designed to cater to a diverse range of users seeking a simple yet powerful task management solution.  
These user stories helped shape the functionality and usability of our CLI application, ensuring it meets the needs of its users effectively.  

The target audience for the app includes tech-savvy, goal-oriented, and organized individuals who prioritize personal productivity.  
Furthermore, the app is designed to be inclusive, aiming to accommodate users from diverse geographic regions, cultures, and backgrounds worldwide.


## Application development
This Python CLI application has been developed iteratively, following basic Agile development principles.  
While still in the learning phase of Agile methodologies, I mostly focused on implementing a small number of  
user stories per iteration. Below are examples of some of the user stories that guided the development process:
- As a potential user, I need to register and to set up a user profile.
- As a registered user, I want to be able to delete my acount.
- As a user, I want to clean up the console before I access another user menu option.
- As a user, I want to see clearly the overdue tasks.

The development process faced several challenges, including numerous bugs and the need for code refactoring to adhere  
to the DRY (Don't Repeat Yourself) principles.

During iterations, the overview over the app development was guided using Lucid wireframes like the one shwon below:

![App flowchart](/assets/images/Flowchart_CLI_TODO.png)<br>
<center>*LovinPlans: Lucid flowchart for application development.*</center><br>

[*Back to top*](#)


## Features

### **1. A user-friendly interface**

***LovinPlans*** is a CLI application that provides an intuitive usage experience through console dialogs.  
Short demos for the app usage are provided in the [Usage](#usage) section.

- The app opens with a Main Menu than provides the following options:
    - 1 (User Login): Login of regsitered users via username and password;
    - 2 (Register a new user): Requires a valid username, password and email address to creates a user profile and  
    a dedicated user worksheet for storing the tasks;
    - 3 (Help): Show the help menu content for running the application;
    - 4 (Exit): Gracefully exiting the application.

![Main menu](/assets/images/start-screen.webp#center)
*<center><font color="red">LovinPlans</font>: App initialization and main menu configuration*.</center><br>

- After the Login, the User Menu section handles the following options for the registered users:
    - 1 (View tasks): List all tasks;
    - 2 (Add task): Add a new task;
    - 3 (Delete task): Delete a task;
    - 4 (Delete account): Delete user account;
    - 5 (Exit): Return to the main menu.

![User menu](/assets/images/user-login-1.webp) <br>
*<font color="red">LovinPlans</font>: User menu configuration.*<br>

- In addition, the users can invoque forced exit by entering 'exit' from the keyboard instead of the suggested options.  
    In the script, the forced exit calls the sys.exit(0) Python routine to close the app gracefully.
- The app is user-friendly and easy to start using without a steep learning curve. To assist new users, the Main Menu includes  
    a Help Menu option that offers a quick tour of the app's functionality (more details in the [Help Menu](#help-menu) section).


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

- provide user worksheets for storing the user login information and contact details such as:
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

![Register new user](/assets/images/register-user.webp) <br>
*<font color="red">LovinPlans</font>: New user registration.*<br>

![Register new user](/assets/images/delete-account.webp) <br>
*<font color="red">LovinPlans</font>: User account deletion.*<br>


### **4. Task Creation and Editing**
- Users can effortlessly create new tasks and edit existing ones with just a few clicks.
- The process of creating a new task requires:
    - a (non-empty) text input of maximum 35 characters
    - a due date specification using the MM-DD-YYYY formatting (e.g., 12-30-2024)
- By default, all newly created tasks receive an 'active' status
- The current local time is also registered in the user worksheet to allow tracking of the overdue tasks.



### **5 Task Views**
- The user tasks are printed on the terminal using the tabulate Python module that allows formatting the output as a table.
- The task viewing functionality is also available for listing the available tasks before selecting the ones to be removed.

![Tasks view](/assets/images/view-tasks.webp) <br>
*<font color="red">LovinPlans</font>: Printing the user tasks on the Herou console.*<br>

### **Clear the terminal option**
- After each main operation such views or multiple entries during user registation or task deletion, the app provides the option  
to clear the terminal to eliminate the cluttering provide a positive UX to the user.
- This also allows the user to stay logged in and explore the app's functionality without being constrained by the terminal height.

![Clear terminal](/assets/images/clean-console.webp) <br>
*<font color="red">LovinPlans</font>: Option to clear the terminal.*<br>

### **6. Help Menu**
- The Help Menu provides a quick overview of the main app functionality.
- The Help Menu content was printed using the user_help() function that opens and writes a Markdown file in the console, as described
[**here**](https://rich.readthedocs.io/en/stable/console.html).

![Help menu](/assets/images/help-menu.png)<br>
*<font color="red">LovinPlans</font>: Help menu content.*<br>

### **7. Task follow up**
- The app allows users to enter task details such as the due date.
- At login, the due date of each user task is checked against the curent date.
- If a task has passed its due date, the task status changes from 'active' to 'overdue', and the overdue tasks are marked using  
    light red color background in the worksheet.

### **8. Menu Navigation**
- The app allows users to switch between menu options without exiting the application using recursive function calls.

### **9. Exception Handling**
- A great deal of attention was put on handling exceptions in order to provide a positive UX.
- The exception handling was implemented using try-except blocks for detect error during executions and provide relevant  
    error messages to the user.
- The expected app behaviour is to remain in the loop until the correct input has been introduced by the user.

Exception handling examples:

![User menu](/assets/images/exception-handling-username-password.webp) <br>
*<font color="red">LovinPlans</font>: Exception handling for wrong username and/or password at Login.*<br>


![User menu](/assets/images/exception-handling-date-format.webp) <br>
*<font color="red">LovinPlans</font>: Exception handling for wrong date format.*<br>

![User menu](/assets/images/exception-handling-user-menu-choice.webp) <br>
*<font color="red">LovinPlans</font>: Exception handling for invalid user menu choice.*<br>


### **10. Cross-Platform Accessibility**
- The app can be used on any device (mobile, tablet, laptop/desktop) that is connected to internet.


[*Back to top*](#)


## Technologies Used
The app was written in Python 3.11.7 version using an external VSCode IDE on a Windows 11 desktop.  
The script utilizes a functional design approach that adheres to the DRY (Don't Repeat Yourself) principles.  
The structure of the app is provided in the [run.py file](run.py) that containts the Python script for  
running the CLI application.

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


### Python modules
The application uses the following external Python modules:
- gspread 6.1.0 ([Python API for Google Sheets](https://docs.gspread.org/en/v6.0.0/))
- gspread_formatting 1.1.2 ([Complete Google Sheets formatting support for gspread worksheets](https://pypi.org/project/gspread-formatting/))
- google-auth 2.29.0 ([Google Auth Library for Python](https://google-auth.readthedocs.io/en/master/))
- google-auth-oauthlib 1.2.0 ([Google Authentication Library](https://pypi.org/project/google-auth-oauthlib/))
- regex 2024.5.10 ([Alternative regular expression module, to replace re.](https://pypi.org/project/regex/))
- rich 13.7.1 ([Python library for writing rich text](https://rich.readthedocs.io/en/stable/introduction.html))
- tabulate 0.9.0 ([Pretty-print tabular data](https://pypi.org/project/tabulate/))

The extrenal modules were installed locally via `pip install` command in the VSCode PowerShell.


### Google Sheets
- The application uses Google Sheets for storage and retrieval of user information.
- The `google-auth` and `google-auth-oauthlib` Python modules are used for authorization and authentication
- The API calls are run performed using the gspread and gspread_formatting Python modules

### Local Development and deployment
The application developement was done using the The Visual Studio Code ([`VScode`](https://code.visualstudio.com/)) IDE version 1.89.1.  
with the [Microsoft Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) installed.  
The `VScode` linters [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) and [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)  
were manually installed and used for checking the Python code style follows the PEP8 conventions.


The app can be run locally (VSCode) using the
```
python run.py
```
command in the terminal.


### Markdown
The Markdown formatting for README.md and HELP.md files was done according to the documentation provided at
[www.markdownguide.org](https://www.markdownguide.org/basic-syntax/).


### Cloud deployment
The app is currently deployed on [Heroku Cloud Application Platform](https://www.heroku.com)
For cloud deployment, the [dependency requirements file](requirements.txt) was compiled using the
```
pip freeze > requirements.txt
```
command in the terminal (VSCode).

The app is currently deployed on github and can be accessed at: https://love-planning-cli-f243068a58dc.herokuapp.com/.

[*Back to top*](#)


## Usage
- The user registraton process: [***here.***](assets/giffs/user-registration.gif)
- Adding and removing tasks: [***here.***](assets/giffs/user-login-add-delete-task.gif)
- Deleting user account: [***here.***](assets/giffs/delete-account.gif)



[*Back to top*](#)


## Manual testing:

| Feature | Expected behaviour | Test | Status |
| --- | --- | --- | --- |
| `User login` | **User information retrieved, registered user can login**
| &nbsp;&nbsp;- *Username validation* | Accept a valid username | Non-empty user input | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Username validation* | Username matched in 'users' worksheet | Entry new valid usernames and existing usernames | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Password validation* | Accept a valid password | Min. 8 characters, 1 capital letter, 2 numerals |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Password validation* | Password matched in 'users' worksheet | Entry valid and invalid passwords for registered users |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Email validation* | Accept a valid email address | Valid format (name, @, and domain) |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Email validation* |Email address matched in 'users' worksheet | Entry valid and invalid emails for registered users |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the user inputs are not valid | Entry valid and invalid user inputs and check if the correct exceptions are raised|![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `User registration` | **New user can open account and login**
| &nbsp;&nbsp;- *Username validation* | Accept a valid username | Non-empty user input | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Password validation* | Accept a valid password | Min. 8 characters, 1 capital letter, 2 numerals |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Email validation* | Accept a valid email address | Valid format (name, @, and domain) |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the user inputs are not valid | Entry valid and invalid user inputs and check if the correct exceptions are raised|![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Add a new task` | **User can add a new task**
| &nbsp;&nbsp;- *Task description* | Accept a valid task description | Check and raise error for empty input, text length between 3-35 characters |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Due date validation* | Accept a valid due date | Check and raise error for invalid date format or for past dates |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Task update* | Increment number of tasks and task ID in 'users' sheet | Check for task id increment when adding new tasks |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Task status* | Mark overdue tasks | Check for change of the cell background color from <span style="background-color:white"><span style="color:white">&nbsp;&nbsp;&nbsp;&nbsp;</span></span> to <span style="background-color:rgb(255, 132, 136)"><span style="color:rgb(255, 132, 136)">&nbsp;&nbsp;&nbsp;&nbsp;</span></span> for the overdue tasks |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the user inputs are not valid | Entry valid and invalid user inputs and check if the correct exceptions are raised|![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Delete task` | **User can remove a task**
| &nbsp;&nbsp;- *User confirmation* | Delete task after user confirmation or continue to `User menu` | Select `Delete task` option and use the `y(Yes)` and `n(No)` user confirmation |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Task list update* | Decrement number of tasks in 'users' sheet, and update task ID in the user's private sheet | Delete user one or more tasks and check the results |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the choice for task deletion is not valid | Entry valid and invalid user inputs and check if the correct exceptions are raised |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Delete user account` | **User can delete its own account**
| &nbsp;&nbsp;- *User confirmation* | Account deleted after user confirmation or continue to `User menu` | Check if task is deleted if for `y(Yes)` user confirmation; check for return to `Usermenu `if `n(No)` is selected |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Delete private user worksheet* | Delete the user worksheet after user confirmation| Check if right user worksheet is deleted using correct and wrong worksheet names |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Delete info from 'users' worksheet* | Delete user information and update the 'users' sheet after account deletion| Delete user account and check for the correct changes |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the selections are not valid | Entry valid and invalid user selections and check if the correct exceptions are raised |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Clear the terminal` | **User can clear the terminal**
| &nbsp;&nbsp;- *User confirmation* | Optional console cleared after user confirmation, or continue to `User menu` | Enter `y/n` options and check results |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the user inputs are not valid | Entry valid and invalid user inputs and check if the correct exceptions are raised |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Application exit (Menu option)` | **User can clear the terminal**
| &nbsp;&nbsp;- *Exiting from the `Main Menu`* | Exit app after user confirmation (yes/no) | Enter `y/n` inputs and check if the application exits or stays in the loop |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *Exiting from the `User Menu`* | Exit app after user confirmation (yes/no) | Enter `y/n` inputs and check if the application exits or stays in the loop |![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `Forced exit` | **User can force the App to exit with the menu Exit option**
| &nbsp;&nbsp;- *Exiting the app from the `Main Menu`* | App exits when the user enters the digit indicated by the `Exit`- menu option | Check if the user input corresponds to the `Exit`- menu option; exit for correct input, or stays in the loop otherwise | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| &nbsp;&nbsp;- *App awaits for valid input* | Error message sent to the user if the `y/n` user input are not valid | Test the `y/n` behaviour for valid and invalid inputs |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `User action feedback` | **User receives a success message after an action is completed**
| &nbsp;&nbsp;- *Message is printed on the console* | Success message sent to the user | Test if the messages appear after task completion |![warning](https://via.placeholder.com/10/00FF00?text=+) `pass`|
| `PEP8 code style conventions` | **Code syle follows the PEP8 conventions**
| &nbsp;&nbsp;- *`CI Python Linter` compatibilty* | Feedback on code quality according to PEP8 conventions | Python code tested using the [CodeInstitute test service](https://pep8ci.herokuapp.com/#) | ![pass](https://via.placeholder.com/10/00FF00?text=+) `pass` `All clear, no errors found`|
---

[*Back to top*](#)

### Additional testing

#### Devices and browsers
Additional testing was performed by calling the application from my private devices operating on Windows 11 (desktop and laptop),  
as well as on a smartphone (Samsung Galaxy S21) operating on Android OS, using the following web browsers:
- Google Chrome: Version 129.0.6668.101 (Official Build) (64-bit)
- Brave: version 1.70.126 Chromium: 129.0.6668.100 (Official Build) (64-bit)
- Microsoft Edge: Version 130.0.2849.46 (Official build) (64-bit)

Using the app on mobiles provides affects the UX due to difficulties with taking the inputs from user when using the mobile keyboard,  
and the poor text visibility.

## <font color="red">Known bugs and issues</font>
- Switching back to the Main Menu from the User Menu not implemented yet;
- In rare situations, the app may exit ungracefully due to API call issues.

If you encounter issues or bugs, please create an issue by clicking [here](https://github.com/eneliviu/LovePlanningCLI/issues).

[*Back to top*](#)

## Possible improvements

### Contact the user
- Functionality to retrieve or change the username and password may be implemented, but the application security has to be enhanced to protect the user privacy

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

[*Back to top*](#)

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

[*Back to top*](#)

## License
### Open Source
As an open-source project, ***LovinPlans*** encourages transparency, and community involvement.

The code is available on GitHub, such that developers can view, fork, and contribute to the project if they wish so.

[*Back to top*](#)

## Acknowledgements
- Further details on the usage of Google Sheets API were obtained from https://developers.google.com/sheets/api/quickstart/python
- Printing the Markdown file in the console used for the Help-menu followed the expamples provided at https://rich.readthedocs.io/en/stable/console.html
- Formatting the worksheet cell background color followed the examples from https://gspread-formatting.readthedocs.io/en/latest/#
- The use of ChatGPT was restricted to getting sensible inputs for the text content in the Readme-file and for proof-checking the language.

[*Back to top*](#)

## Documentation version
Last updated: October 19, 2024

[*Back to top*](#)