
#%%
#=================================================================#
# Write your code to expect a terminal of 80 characters wide and 24 rows high
#=================================================================#

from datetime import datetime
import gspread 
from gspread_formatting import *
from google.oauth2.service_account import Credentials
import regex as re
import os
import regex as re
from rich.console import Console
from rich.markdown import Markdown
import sys
from tabulate import tabulate
from typing import Tuple

#=================================================================#

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('LovePlanning')

USERS = 'users'
TASKS = 'tasks'
STATIC_OPTIONS = ['y', 'n']
USER_HEADER = ['user_id', 'user_name', 'email', 'password', 'tasks']
TASK_HEADER = ['task_id', 'description', 'category', 'created', 'due', 'status']
TASK_CATEGORY = ['errand', 'personal', 'work']

#=================================================================#
# --------------------- For New Users: ---------------------------#

#%%

def smooth_exit(user_exit_input:str) -> None:
    '''
    Kill the application when the user enters 'exit'. 
    The input string is converted to lowercase.
    '''

    if user_exit_input.lower() == 'exit':
            print('Operation canceled! You are logged out.\n')
            sys.exit(0)

def validate_static_options(remove_choice:str, options:list[str]) -> bool:
    '''
    Check if the user inputs are either y (Yes) or n (No). 
    The input strings are converted to lower case.
    '''
    while True:

        # Smooth application exit:
        smooth_exit(remove_choice)

        if remove_choice.lower() not in options:
            remove_choice = input('Invalid option: please press y(Yes) to proceed, or n(No) to return.'
                                '(Enter Exit to cancel): \n')
        else:
            break
            
    return True

def clean_cli() -> None:
    '''
    CLean the console. Works for Windows and Linux OS.
    '''
# https://www.geeksforgeeks.org/clear-screen-python/
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def clear_output(clean_cli_choice:str) -> None:
    '''
    Validates the user option to clear the terminal.
    '''
    if validate_static_options(clean_cli_choice, STATIC_OPTIONS):
        if clean_cli_choice.lower() == 'y': 
            clean_cli()
        
def make_dict_from_nested_lists(list_data:list[list], d_keys:list[str]) -> dict:
    '''
    Takes the google sheet data as list of lists and creates a dictionary using 
    dictionary comprehension.
    - keys: the values in d_keys list argument
    - values: the lists in the list_data argument

    Returns a dictionary. 
    '''

    #list_data.copy().insert(0, d_keys) # shallow list copy to avoid changing the original variable 

    return {d_keys[i]:[s[i] for s in list_data] for i in range(len(d_keys)) }  


#%%

def validate_user_password(**kwargs) -> str:
    '''
    Validate entry password for new users: at least 8 characters length, of which
    at least one capital letter and at least two numerals.
    '''

    while True:
        
        new_user_password = input('Please enter your pasword or Exit to cancel: \n')
        
        # Smooth application exit:
        smooth_exit(new_user_password)
        
        password_length = len(new_user_password)
        capital_letters = len([s for s in new_user_password if s.isupper()])

        try: 
            if password_length < kwargs['length']:
                raise ValueError(
                        f'At least {kwargs["length"]} characters required!'
                    )
            elif password_length >= kwargs['length'] and \
                capital_letters < kwargs['capital_letters']:
                raise ValueError(f'At least one capital letter required!')
            elif password_length >= kwargs['length'] and \
                capital_letters >= kwargs['capital_letters'] and \
                sum([s.isdigit() for s in new_user_password]) < kwargs['digits']:
                raise ValueError(f'At least {kwargs["digits"]} numerals are required!')
            else:
                break 
        except ValueError as e:
            print(f'Invalid password: {e}, please try again.\n')

    return new_user_password

def validate_username(username_column:list[str]) -> bool:
    '''
    Validate the user input for login option:
    - The name and passord strings must not be empty;
    - The input must contain two strings separated by comma;
    It applies to registered users, as well as to new users trying to register.
    '''
    while True:
        new_user_name = input('Please enter your username or Exit to cancel: \n')
        
        # Smooth application exit:
        smooth_exit(new_user_name)


        try: 
            if len(new_user_name) == 0:
                raise ValueError('Username must not be empty')
            elif new_user_name in username_column[-1]:
                raise ValueError('Username not available')
            else:
                break
        except ValueError as e:
            print(f'{e}. Please try again!')
            return False
    
    return new_user_name

def validate_user_email(user_email_column:list[str]) -> bool:
    '''
    Check if the string contains a valid email address 
    using regular expressions (regex).
    https://www.w3schools.com/python/python_regex.asp 
    '''
    
    valid_pattern = r"^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

    while True:
        new_user_email = input('Enter your email address or Exit to cancel: \n')
        
        # Smooth application exit:
        smooth_exit(new_user_email)


        try: 
            if re.search(valid_pattern, new_user_email) is None:
                raise ValueError('Please enter a valid email address')
            elif new_user_email in user_email_column[-1]:
                raise ValueError('Email address not available')
            else:
                break
        except ValueError as e:
            print(f'{e}. Please try again!')

    return new_user_email

def create_new_user_worksheet(new_user_data:dict) -> None:
    '''
    Validates username and password for new users by matching them against the
    records of the rehistered users in the 'users' sheet. The new user credentials
    should not be found aming the credentials of the existing users. Passwords are not
    mached against the registered ones, since that would be a security break.
    Dictionary keys:
    - user row index: int
    - user_name: str
    - user_email: str
    - password: str
    - number of tasks: int
    
    Returns a the dictionary containing the new user credentials.  
    '''
    
    # Create a new worksheet having the username as its name.    
    SHEET.add_worksheet(title = new_user_data['user_name'], rows = 1000, cols = len(TASK_HEADER))

    # Write the default worksheet column names:
    SHEET.worksheet(new_user_data['user_name']).append_row(TASK_HEADER)

    # Append the user informatin row to the worksheet:
    SHEET.worksheet(USERS).append_row(list(new_user_data.values()))


def new_user_registration() -> dict:
    '''
    Validates credentials (username and password) from user input.
    - The while-loop runs until the user enters the correct data. 
    - Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data (without header)
    ''' 

    # Retrieveing columnwise data sequentially takes longer time, 
    # but it can be eventually implemented asyncroniously.   
    username_column, _ = get_column(SHEET.worksheet(USERS), 'user_name', USER_HEADER)
    user_email_column, _ = get_column(SHEET.worksheet(USERS), 'email', USER_HEADER)
    
    new_user_name = validate_username(username_column)
    new_user_password = validate_user_password(length=8,
                                            capital_letters=1,
                                            digits=2)
    new_user_email = validate_user_email(user_email_column)

    new_user_data = [len(username_column), 
                        new_user_name,
                        new_user_email,
                        new_user_password,
                        0]
    new_user_data = dict(zip(USER_HEADER, new_user_data))

    create_new_user_worksheet(new_user_data)
    
    
    print('Registration successful!\n')
            
    return new_user_data

#%%
#=================================================================#
# ------------------- For Registered Users: ----------------------#

def validate_login_input() -> bool:
    '''
    Check if the user log input contains two non-empty strings 
    (username and passord) separated by comma. 
    '''
    user_input = input('Enter username and password separated by comma or Exit to cancel: \n')
    
    # Smooth application exit:
    smooth_exit(user_input)

    
    try:
        if len(user_input) == 0:
            raise ValueError('Enter username and password separated by comma')
        elif user_input.find(',') < 0:
            raise ValueError('Use comma to separate username and password')
        else:
            user_input = user_input.split(',')
            if len(user_input[0]) == 0 and len(user_input[1]) == 0:
                raise ValueError('Username and Password cannot be empty')
            elif len(user_input[0].strip()) == 0:
                raise ValueError('Username cannot be empty')
            elif len(user_input[1].strip()) == 0:
                raise ValueError('Password cannot be empty')
            else:
                return user_input
    except ValueError as e:
            print(f'{e}. Please try again!')
            return False

def match_user_credentials(user_data:dict, user_name:str, user_password:str) -> bool:
    '''
    Validates existing username and passowrd by matching them against the
    user records in the 'users' sheet. Returns a bool (True/False)  
    '''
    
    if user_name == user_data['user_name'] and \
        user_password == user_data['password']:   
        return True
    elif user_name != user_data['user_name'] and \
            user_password != user_data['password']:
        print('Username and password not found, please try again')
        return False
    elif user_name != user_data['user_name']:
        print('Username not found, please try again')
        return False
    elif user_password != user_data['password']: 
        print('Password not found, please try again')   
        False
    else:
        return False


def get_sheet_meta(worksheet_name:str) -> list:
    '''
    Retreave a worksheet and its header.
    '''

    # Connect to the Worksheet:
    wksheet = SHEET.worksheet(worksheet_name)
    # Read the heaser (first row):
    wksheet_header = wksheet.row_values(1)
    return wksheet, wksheet_header

def get_column(worksheet:gspread.worksheet.Worksheet, column_name:str, header:list[str]) -> list[str]:
    '''
    Get the 'user_id' column from a worksheet. 
    Returns a list containing the column header and the values.
    Notice that the for Google Sheets, the row numbers start at 1, while Python list indices start at 0.
    Returns a dictionary with the header values as keys and user records as values.  
    '''
    # Get the 1-based index of the 'user_id' columns
    col_idx = header.index(column_name) + 1
    
    # Get the data in the 'user_id' column
    col_data = worksheet.col_values(col_idx)
    return col_data, col_idx


def get_row(worksheet:gspread.worksheet.Worksheet, users_col:list[str], user_name:str) -> list:
     # Get the index of the username in the column
    user_idx = users_col.index(user_name)+1
    # Retrieve the row containig the user info based n the username index:
    user_info = worksheet.row_values(user_idx)
    return user_info, user_idx


def get_user_info(worksheet_name:str, user_name:str) -> dict:
    '''
    Get the user info from the 'users' worksheet based on 
    the username index. Can be handy when there are many 
    registered users since it does not require to import the 
    entire worksheet data. Notice that the for Google Sheets,
    the row numbers start at 1, while Python list indices start at 0.
    Returns a dictionary with the header values as keys and user records as values. 
    '''
    
    # Connect to the worksheet and retrive the header:
    wksheet = SHEET.worksheet(worksheet_name)
 
    # Get the 'user_name' column from the 'users'-worksheet:
    users_col, _ = get_column(wksheet, 'user_name', USER_HEADER)

    # Retrieve the row containig the user information from 'users'-worksheet:
    user_info, _ = get_row(wksheet, users_col, user_name)

    return dict(zip(USER_HEADER, user_info))


def tasks_list(user_data:dict) -> Tuple[gspread.worksheet.Worksheet, dict]:
    '''
    Takes a dictionary conatining the user information, and returns a tuple containing:
    - the user worksheet (the first element)
    - a dictionary containing the user tasks information (the second element).  
    '''
    
    # Connect to the worksheet
    wksheet = SHEET.worksheet(user_data['user_name'])

    # Get all the row values for the tasks associated to an user_id:   
    task_info = make_dict_from_nested_lists(wksheet.get_all_values()[1:], TASK_HEADER)
    
    return wksheet, task_info


def user_login() -> list:
    '''
    Validates credentials (username and password) from user input.
    - The while-loop runs until the user enters the correct data. 
    - Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data (without header)
    '''
    while True:
        user_input = validate_login_input()

        # Retrieve the input components: username [0] and password [1]
        if user_input:

            user_name = user_input[0].strip()
            user_password = user_input[1].strip()

            # Get the user data from the 'users' Google worksheet:           
            user_data = get_user_info(USERS, user_name)

            if match_user_credentials(user_data, user_name, user_password):
                print('Login successful!')
                
                # Check for overdue tasks at login:
                sort_tasks_by_datetime(SHEET.worksheet(user_data['user_name']))
                break

    return user_data
                    

def user_help() -> None:
    '''
    Opens and writes a Markdown file in the console.  
    https://rich.readthedocs.io/en/stable/console.html
    '''
    console = Console()

    with open("assets/files/HELP.md", "r+") as help_file:
        console.print(Markdown(help_file.read()))

    # markdown_help_text = '''
    #     1. Menu options for registered users:  
    #     - 1 (View tasks):     ---> List all tasks
    #     - 2 (Add task):       ---> Add a new task
    #     - 3 (Delete task):    ---> Delete a task
    #     - 4 (Delete account): ---> Delete user account
    #     - 5 (Exit):           ---> Return to the main menu
    #     2. Menu options for new users  
    #     Registration process requires the following information:
    #     - User name (non-empty)            
    #     - User password: minimum 8 characters, of which at least one
    #         capital letter and two numerals
    #     - Valid email address (e.g., someone@somewhere.com)  
    #     3. Datetime entries 
    #     The date entries must be in the MM-DD-YYYY format (e.g., 12-30-2024). 
    #     4. Forced exit 
    #     The forced application exit can be triggered by entering "exit".
    #     5. To clean the terminal, confirm y (Yes) when the prompt requires to do so.
    #     Press n (No) otherwise.   
    # '''
    # console = Console()
    # md = Markdown(markdown_help_text)
    # console.print(md)
    

def check_overdue_task(worksheet:gspread.worksheet.Worksheet, overdue_rows:list) -> None:  
    '''
    Check if a task is overdue by comparing the due date of the task with the current date-time.
    Changes the task status from 'active' with 'overdue', and sets the cell background colour to red.
    '''
    # Format cell background color using RGB values as floats (1 is full intensity, 0 is no intensity):
    ## https://gspread-formatting.readthedocs.io/en/latest/#
    fmt = CellFormat(backgroundColor = color(1, 0.9, 0.9))

    # Update task status for overdue tasks:
    for k in overdue_rows:
        worksheet.update_cell(k, TASK_HEADER.index('status') + 1, 'overdue')
        cell_in_worksheet = gspread.utils.rowcol_to_a1(k, TASK_HEADER.index('status') + 1)
        format_cell_range(worksheet, cell_in_worksheet, fmt)


def sort_tasks_by_datetime(worksheet:gspread.worksheet.Worksheet) -> bool:
    due_date_col, _ = get_column(worksheet, 'due', TASK_HEADER)
    due_dates_tasks = [datetime.strptime(d, "%m-%d-%Y").date() for d in due_date_col[1:]]
    due_dates_tasks_ordered = sorted(due_dates_tasks)
    due_date_idx = [due_dates_tasks.index(d) for d in due_dates_tasks_ordered]
    overdue_task_row = [ i + 2 for i in range(len(due_dates_tasks_ordered)) if due_dates_tasks_ordered[i] < datetime.now().date()]
    
    if len(overdue_task_row) > 0:
            check_overdue_task(worksheet, overdue_task_row)
    
    if due_dates_tasks_ordered != due_dates_tasks:
        unsorted_task = worksheet.get_all_values()[1:] 
        sorted_task = [unsorted_task[idx] for idx in due_date_idx]
        worksheet.update([TASK_HEADER] + sorted_task)
        return True
    else:
        return False


def validate_task_index(tasks_idx:list[int]) -> bool:
    
    task_remove_idx = input('Please enter the indexes for tasks to be removed.'
                            'Use commas to separate multiple entries.'
                            '(Enter Exit to cancel): \n')
    
    

    while True:

        # Smooth application exit:
        smooth_exit(task_remove_idx)

        if len(task_remove_idx) == 1:
            task_remove_idx = list(task_remove_idx)
    
        if sum([True for k in task_remove_idx if k in tasks_idx]) == len(tasks_idx):
            break
        elif len(tasks_idx) == 0:
            print('There are no tasks to remove!')
            return False
        else:
            task_remove_idx = input('Please enter the indexes for tasks to be removed.'
                        'Use commas to separate multiple entries.'
                        '(Enter Exit to cancel): \n'
                        )
    
    return task_remove_idx


def delete_task(user_data:dict, worksheet:gspread.worksheet.Worksheet, user_task_data:dict) -> None:
    '''
    Delete one or more selected tasks.
    The function removes the rows corresponding to the selected tasks from the 'tasks'Google worksheet.
    The task IDs separated by commas are entered by the user.
    After input validation, the task deletion awaits for confirmation (yes or no) in order to proceed.
    After completion, the user returns to the main menu.
    
    Arguments:
    - user_data:     ---> dictionary with user the information from the 'users'-worksheet
        - keys: user_id, user_name, email, password and tasks 
    - user_task_data ---> dictionary with the user task information 
        - keys: task_id, description, category, created, due and status
    '''

    
    
    # Check that user input task index corresponds with the task indexes from the worksheet:
    task_remove_idx = validate_task_index(user_task_data['task_id'])

    # Confirm the choice:
    remove_choice = input(f'You selected task {task_remove_idx} to be removed.'
                            'Press Yes(y) to proceed, No(n) to cancel: \n')
    
    # If the user inputs are valid, delete task(s) and update the remaining task_id cells 
    # to start from 1: 
    if validate_static_options(remove_choice, STATIC_OPTIONS):
        if remove_choice.lower() == 'y':
            task_remove_idx = sorted(list(set([int(k) for k in task_remove_idx.split(',')])))
            #user_row_remove_idx = [i - 1 for i in task_remove_idx]

            # Update the worksheet:
            ## Delete one row (task) at a time:      
            reduce_idx = 0
            for k in range(len(task_remove_idx)):
                row_to_delete = task_remove_idx[k] + 1 - reduce_idx
                worksheet.delete_rows(row_to_delete)
                print(f'Task {k} deleted...Row {row_to_delete} deleted.')
                reduce_idx += 1
            
            ## Check if there is any task left, otherwise exit function:
            taskid_col, column_id = get_column(worksheet, 'task_id', TASK_HEADER) 
            
            if len(taskid_col[1:]) == 0: # No more tasks left:
                print('All task were removed!')
                
                # Update the cell containing the # of tasks in the user row form the 'user'-worksheet:
                SHEET.worksheet(USERS).update_cell(int(user_data['user_id'])+1, 
                                    USER_HEADER.index('tasks') + 1,
                                    str(len(taskid_col[1:])))
                return
            
            ## If there are more tasks left, make sure they are sorted ascending by due date and 
            ## get the task id column info: 
            if sort_tasks_by_datetime(worksheet):
                taskid_col, column_id = get_column(worksheet, 'task_id', TASK_HEADER)

            ## If there are more tasks left, make sure the task_id is updated:
            for k in range(len(taskid_col[1:])):    
                worksheet.update_cell(k + 2, column_id, k+1)

            # Update the cell containing the # of tasks in the user row form the 'user'-worksheet:
            SHEET.worksheet(USERS).update_cell(int(user_data['user_id'])+1, 
                                            USER_HEADER.index('tasks') + 1,
                                            str(len(taskid_col[1:])))

            print(f"Tasks deleted: {len(task_remove_idx)} --- Tasks left: {len(taskid_col[1:])}.")

    else:
        print('Operation cancelled.')     


def delete_account(user_name:str) -> bool:
    '''
    Delete the user account in the following order:
    - removes the user info from the 'users'-worksheet
    - updates the 'user_id' column from the 'users'-worksheet
    - removes the worksheet containing the user tasks
    
    The deletion cannot be undone. 
    '''
    
    remove_choice = input('Your account will be permanently deleted.'
                        'Press Yes(y) to proceed, No(n) to cancel: \n')
    
    if validate_static_options(remove_choice, STATIC_OPTIONS):
        if remove_choice.lower() == 'y':

            # Remove the row containing the user information from the 'users'-worksheet:
            user_data = get_user_info(USERS, user_name)
            user_column, _ = get_column(SHEET.worksheet(USERS), 'user_name', USER_HEADER)
            _, row_index = get_row(SHEET.worksheet(USERS), user_column, user_data['user_name'])
            SHEET.worksheet(USERS).delete_rows(row_index)

            # Update the 'user_id'-column from the 'users'-worksheet:
            user_id_column, column_idx = get_column(SHEET.worksheet(USERS), 'user_id', USER_HEADER)
            user_id_column[1:] = [i + 1 for i in range(len(user_id_column[1:]))]

            for i in range(len(user_id_column[1:])):
                SHEET.worksheet(USERS).update_cell(i + 2, column_idx, user_id_column[i + 1])

            # Remove the user worksheet:
            SHEET.del_worksheet(SHEET.worksheet(user_data['user_name']))

            print('The account was deleted!')
            return True

        else:
            print('Operation cancelled.')
            return False 


def validate_new_task_description() -> list[str]:
    '''
    Validates the task description entry. The task description
    must be non-empty and have at most 70 characters. 
    '''
    while True:
        
        new_task = input('Enter a new task (maximum 70 characters): \n')
        
        # Smooth application exit:
        smooth_exit(new_task)

        if len(new_task) == 0 :
            print('A new task cannot be empty. Please try again.')
        elif len(new_task) > 70:
            print(f'The task contains {len(new_task) - 70} extra characters. Please try again.')
        else:
            break
        
    return new_task


def validate_new_task_category() -> list[str]:
    '''
    Checks that the task category entry is either 'errand', 'personal', or 'work'.
    Casts all inputs to string to avoid checking for numerals.   
    '''
    while True:
        task_category = input('Specify the task category (errand, personal, or work): \n')
        
        # Smooth application exit:
        smooth_exit(task_category)

        if str(task_category).lower().strip() not in TASK_CATEGORY:
            print('Invalid choice. Please select a valid category (errand, personal, or work): ')
        else:
            break       
    
    return task_category


def validate_due_date() -> datetime:
    '''
    Checks if the datetime input provides the valid day, month and year values in the 
    requested format MM-DD-YYY (e.g., 05-15-2024), otherwise it throws a ValueError.
    The due date also has to be past the current time.
    '''

    while True:
        due_date = input('Enter the due date in the MM-DD-YYYY format\n'
                        '(Enter Exit to cancel): \n')
        
        # Smooth application exit:
        smooth_exit(due_date)

        creation_date = datetime.now().date()
        try:
            due_date = datetime.strptime(due_date, "%m-%d-%Y").date()
            try:
                if due_date < creation_date:
                    raise ValueError('The date is prior to the current time')
                break
            except ValueError as e:
                print(f'Invalid time. {e}.')
        except ValueError as e:
            print('Please enter a date in MM-DD-YYYY format.')

    return due_date.strftime("%m-%d-%Y"), creation_date.strftime("%m-%d-%Y")


def add_task(user_data:str) -> None:
    '''
    Add a new task to the user worksheet. The new task is inserted such that 
    it maintains the default sorting by due date, with the earliest due date at the top. 
    '''

    #_, task_row = tasks_list(user_data)
    user_data = get_user_info(USERS, user_data['user_name'])

    task_row = dict.fromkeys(TASK_HEADER)
    task_row['description'] = validate_new_task_description()
    task_row['category'] = validate_new_task_category() 
    task_row['due'], task_row['created'] = validate_due_date()
    task_row['status'] = 'active'
    task_row['task_id'] = str(int(user_data['tasks']) + 1)
    task_info = list(task_row.values())
    
    #print(tabulate([task_info], headers=TASK_HEADER))
    #print(tabulate(task_row, headers="keys", numalign="center"))

    SHEET.worksheet(user_data['user_name']).append_row(task_info)
    
    # Keep the tasks sorted ascedning by due date.
    # If not sorted, then sort and update the task indexes. 
    if sort_tasks_by_datetime(SHEET.worksheet(user_data['user_name'])): 
        taskid_col, column_id = get_column(SHEET.worksheet(user_data['user_name']),
                                            'task_id',
                                            TASK_HEADER)
        for k in range(len(taskid_col[1:])):    
            SHEET.worksheet(user_data['user_name']).update_cell(k + 2, column_id, k+1)


    # Update the  number of tasks in the 'tasks' column from the 'users'-worksheet:
    user_column, _ = get_column(SHEET.worksheet(USERS), 'user_name', USER_HEADER)
    user_row, row_index = get_row(SHEET.worksheet(USERS), user_column, user_data['user_name'])
    user_row = dict(zip(USER_HEADER, user_row))
    user_row['tasks'] = str(int(user_row['tasks']) + 1)

    # Update user row:
    _, column_index = get_column(SHEET.worksheet(USERS), 'tasks', USER_HEADER)
    SHEET.worksheet(USERS).update_cell(row_index, column_index, int(user_row['tasks']))

    return dict(zip(TASK_HEADER, task_info))


def main_menu() -> int:
    '''
    Gets user choices as follows:
    - 1 : User Login
    - 2 : Register a new user
    - 3 : Show the help content for running the application
    - 4 : Exit the application

    Runs a while loop to collect a valid string of data
    from the user via the terminal. The loop breaks
    when the user input data is valid.
    
    Returns an integer in range 1-4. 
    '''
    while True:
        input_option = input('Select: 1 (User Login), 2 (Register User), 3 (Help), 4 (Exit): \n')
        
        # Smooth application exit:
        smooth_exit(input_option)

        if not input_option.isdigit():
            print('Invalid choice!\n'
                'Valid options: 1 (User Login), 2 (Register User), 3 (Help), 4 (Exit): ')
        elif input_option.isdigit() and int(input_option) not in range(1, 5):
            print('Invalid choice!\n'
                'Valid options: 1 (User Login), 2 (Register User), 3 (Help), 4 (Exit): ')
        else:
            break

    return int(input_option)


def handle_input_options(input_option:int) -> None:
    '''
    Takes the menu selection from user input and handles the menu item logic:
    - 1 : User Login
    - 2 : Register a new user
    - 3 : Show the help content for running the application
    - 4 : Exit the application
    '''
    while True:
        if input_option == 1: # USER LOGIN
            user_data = user_login()
            task_handler(user_data)  # takes user_id and returns the user tasks
            break
        elif input_option == 2: # REGISTER NEW USER
            user_data = new_user_registration()
            task_handler(user_data) 
            break
        elif input_option == 3: # HELP MENU
            clear_output('y')
            user_help()
            clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise.\n'
                            '(Enter Exit to cancel): \n'))
            handle_input_options(main_menu())
        else: # Exit app
            print('You are now logged out.\n')
            sys.exit(0)

def task_handler(user_data:dict) -> None:
    '''
    Handles the menu options for registered users:
    * 1 (View tasks):     ---> List all tasks
    * 2 (Add task):       ---> Add a new task
    * 3 (Delete task):    ---> Delete a task
    * 4 (Delete account): ---> Delete user account
    * 5 (Exit):           ---> Return to the main menu
    The function uses a recursive call to return to the user menu after completing a task. 
    '''
    print('\nSelect an option:')
    print('1 (View tasks), 2 (Add task), 3 (Delete task), 4 (Delete user account) 5 (Exit): ')

    while True:
        user_choice = input()
        if not user_choice.isdigit():
            print('Invalid selection! Please select a valid option:')
            print('1 (View tasks), 2 (Add task), 3 (Delete task), 4 (Delete user account) 5 (Exit).')
        elif int(user_choice) not in range(1, 6):
            print('Invalid selection! Please select a valid option:')
            print('1 (View tasks), 2 (Add task), 3 (Delete task), 4 (Delete user account) 5 (Exit).')
        else:
            user_choice = int(user_choice)
            if user_choice == 1: # View tasks
                tasks, task_info = tasks_list(user_data)
                if int(user_data['tasks']) == 0:
                        print('You have no scheduled tasks.\n')
                        clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))
                        task_handler(user_data)
                else:
                    print('Your tasks are listed below:')
                    print(tabulate(task_info, headers="keys", numalign="center"))
                    clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))
                    task_handler(user_data)
            elif user_choice == 2: # Add a new ask
                add_task(user_data)
                task_handler(get_user_info(USERS, user_data['user_name']))
            elif user_choice == 3: # Delete task
                tasks, task_info = tasks_list(user_data)
                print('Your tasks are listed below:')
                print(tabulate(task_info, headers="keys", numalign="center"))
                delete_task(user_data, tasks, task_info)
                clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))
                task_handler(get_user_info(USERS, user_data['user_name']))
            elif user_choice == 4: # Delete user account
                account_deleted = delete_account(user_data['user_name'])
                if account_deleted:
                    sys.exit(0)
                    #break
                else:
                    task_handler(user_data)
            else:
                print('You are now logged out.\n')
                sys.exit(0)


#%%                
# The main() function to run the app:
def main() -> None:
    '''
    The main() function that wraps all the other functionality required to run the app.
    '''

    print(  '*******************************************************************\n'
            '*** Welcome to LovePlanning, the Ultimate Task Management Tool! ***\n'
            '*******************************************************************\n')

    while True:
        # Try-except block at the top of the call stack to handle API call errors
        # and exit gracioulsy if that happens: 
        try: 
            if not handle_input_options(main_menu()):
                print('You are now logged out.\n')
                break
        except gspread.exceptions.APIError as e:
            print(f' An API error has occured: {e}.\n'
                'Exiting application....')
            sys.exit(1) 

# %%

# Run the App:

main()

