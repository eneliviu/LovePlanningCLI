
#%%
#=================================================================#
# Write your code to expect a terminal of 80 characters wide and 24 rows high
#=================================================================#

from datetime import datetime
import gspread 
import gspread_formatting as gf
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

# Declare constants:
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
TASK_HEADER = ['task_id', 'description', 'created', 'due', 'status']

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

    Returns a bool.
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
    Clean the console. Works for Windows and Linux OS.
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

    Returns a dictionary:
    - keys:str ---> d_keys 
    - values:list[list] ---> list_data
    '''

    return {d_keys[i]:[s[i] for s in list_data] for i in range(len(d_keys)) }  


#%%

def validate_user_password(**kwargs) -> str:
    '''
    Validate entry password for new users: at least 8 characters length, of which
    at least one capital letter and at least two numerals.

    Returns a valid input password as a string.
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

def validate_username(username_column:list[str]) -> str:
    '''
    Validate the user input for login option:
    - The name and passord strings must not be empty;
    - The input must contain two strings separated by comma;
    It applies to registered users, as well as to new users trying to register.

    Returns a vlid user name as a string.
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

def validate_user_email(user_email_column:list[str]) -> str:
    '''
    Check if the string contains a valid email address 
    using regular expressions (regex).
    https://www.w3schools.com/python/python_regex.asp 

    Returns a valid email address as a string.
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
    Creates a new worksheet for a newly registerd user that will contain the tasks list.
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
    Internally, it calls the function to create a dedicated worksheet for the new user.

    Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data
            - user_id:row index: int
            - user_name: str
            - user_email: str
            - password: str
            - number of tasks: int

    ''' 

    # Retrieveing columnwise data sequentially takes longer time, 
    # but it can be eventually implemented asyncroniously.   
    username_column, _ = get_column(worksheet=SHEET.worksheet(USERS),
                                    column_name='user_name',
                                    header = USER_HEADER)
    user_email_column, _ = get_column(worksheet = SHEET.worksheet(USERS),
                                    column_name = 'email',
                                    header = USER_HEADER)
    
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

def match_user_credentials(**kwargs) -> bool:
    '''
    Validates existing username and passowrd by matching them against the
    user records in the 'users' sheet.  
    
    Argumens:
    * user_data:dict ---> username and password from the 'users' worksheet 
    * user_name:str  ---> user name input
    * user_password:str ---> user password input

    Returns a bool.
    '''
    
    if (kwargs['user_name'] in kwargs['users_col']) and \
        (kwargs['user_password'] in kwargs['passwords_col']):   
        return True
    elif (kwargs['user_name'] not in kwargs['users_col']) and \
            (kwargs['user_password'] not in  kwargs['passwords_col']):
        print('Username and password not found, please try again')
        return False
    elif kwargs['user_name'] not in kwargs['users_col']:
        print('Username not found, please try again')
        return False
    elif  kwargs['user_password'] not in kwargs['passwords_col']: 
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


def get_column(**kwargs) -> list[str]:
    '''
    Get the 'user_id' column from a worksheet. 
    Returns a list containing the column header and the values.
    Notice that the for Google Sheets, the row numbers start at 1, while Python list indices start at 0.
    Returns a dictionary with the header values as keys and user records as values.
    
    Arguments:
    * worksheet:gspread.worksheet.Worksheet ---> worksheet
    * header:str ---> worksheet header
    * column_name:str ---> username
    '''
    
    # Get the 1-based index of the 'user_id' columns
    col_idx = kwargs['header'].index(kwargs['column_name']) + 1
    
    # Get the data in the 'user_id' column
    col_data = kwargs['worksheet'].col_values(col_idx)

    return col_data, col_idx

def get_row(**kwargs) -> list:
    '''
    Returns a tuple containing a list with row data, and the corresponding row index from a worksheet.
    Notice that the for Google Sheets, the row numbers start at 1, while Python list indexes are 0-based.
    
    Arguments:
    * worksheet:gspread.worksheet.Worksheet ---> worksheet
    * worksheet_column_data:list[str] ---> worksheet column
    * user_name:str ---> username
    '''

    # Get the index of the username in the column
    user_idx = kwargs['worksheet_column_data'].index(kwargs['user_name'])+1

    # Retrieve the row containig the user info based n the username index:
    user_info = kwargs['worksheet'].row_values(user_idx)
    return user_info, user_idx


def get_user_info(**kwargs) -> dict:
    '''
    Returns a dictionary with the user info from the 'users' worksheet. 
    Can be handy when there are many registered users since it does not require 
    to import the entire worksheet data. Notice that the for Google Sheets, 
    the row numbers start at 1, while Python list indexes are 0-based.
    
    Arguments:
    * worksheet_name: str ---> worksheet name
    * column_name:list[str] ---> worksheet column name
    * user_name:str ---> user name
    * header:str ---> column names of the user worksheet (USER_HEADER)
    
    Returns a dictonary:
    - keys:str ---> the worksheet column names 
    - values:str ---> user records.
    
    '''

    try:
        if type(kwargs['worksheet']) == gspread.worksheet.Worksheet:
            wksheet = kwargs['worksheet']

        if type(kwargs['worksheet']) == str:
            wksheet = SHEET.worksheet(kwargs['worksheet']) 
        
    except TypeError as e:
        print(f'Something went wrong: {e}. Please try again!')
        sys.exit(1)

    # Get the 'user_name' column from the 'users'-worksheet:
    users_col, _ = get_column(worksheet = wksheet, #kwargs['worksheet'], 
                                column_name = kwargs['column_name'],
                                header = kwargs['header'])
    
    # Retrieve the row containig the user information from 'users'-worksheet:
    user_info, _ = get_row(worksheet = wksheet, #kwargs['worksheet'],
                            worksheet_column_data = users_col, 
                            user_name = kwargs['user_name'])

    return dict(zip(USER_HEADER, user_info))


def tasks_list(user_data:dict, header:str) -> Tuple[gspread.worksheet.Worksheet, dict]:
    '''
    Retrieves the user tasks. 
    
    Arguments:
    - user_data:dict ---> contains the user information:
        - keys:
        - values
    
    - header: str ---> worksheet column names

    Returns a tuple containing:
    - wksheet:gspread.worksheet.Worksheet ---> user worksheet connection
    - task_info:dict ---> dictionary containing the user tasks:
        - keys:str
        - values:str
    '''
    
    # Connect to the worksheet
    wksheet = SHEET.worksheet(user_data['user_name'])

    # Get all the row values for the tasks associated to an user_id:   
    task_info = make_dict_from_nested_lists(wksheet.get_all_values()[1:], header)
    
    return wksheet, task_info


def user_login(**kwargs) -> list:
    '''
    Validates credentials (username and password) from user input.
    - The while-loop runs until the user enters the correct data. 
    - Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data (without header)

    Arguments:
    - worksheet:
    - 
    '''

        
    # Connect to the worksheet and retrive the header:
    wksheet = SHEET.worksheet(kwargs['worksheet_name'])

    while True:
        user_input = validate_login_input()

        # Retrieve the input components: username [0] and password [1]
        if user_input:

            user_name = user_input[0].strip()
            user_password = user_input[1].strip()

            users_col, _ = get_column(worksheet = wksheet, 
                                        column_name = kwargs['user_column_name'], 
                                        header = kwargs['header'])
            
            passwords_col, _ = get_column(worksheet = wksheet, 
                                column_name = kwargs['password_column_name'],
                                header = kwargs['header'])
            
            if match_user_credentials(users_col = users_col, 
                                        passwords_col = passwords_col, 
                                        user_name = user_name,
                                        user_password = user_password):
                # Get the user data from the 'users' Google worksheet:           
                user_data = get_user_info(worksheet = wksheet,
                                        column_name =  kwargs['user_column_name'], 
                                        user_name = user_name,
                                        header =  kwargs['header'])

                # Check for overdue tasks at login:
                sort_tasks_by_datetime(SHEET.worksheet(user_data['user_name']))

                print('Login successful!')

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


def check_overdue_task(worksheet:gspread.worksheet.Worksheet, overdue_rows:list) -> None:  
    '''
    Check if a task is overdue by comparing the due date of the task with the current date-time.
    Changes the task status from 'active' with 'overdue', and sets the cell background colour to red.

    Returns a bool.
    '''
    # Format cell background color using RGB values as floats (1 is full intensity, 0 is no intensity):
    ## https://gspread-formatting.readthedocs.io/en/latest/#
    fmt = gf.CellFormat(backgroundColor = gf.color(1, 0.9, 0.9))

    # Update task status for overdue tasks:
    for k in overdue_rows:
        worksheet.update_cell(k, TASK_HEADER.index('status') + 1, 'overdue')
        cell_in_worksheet = gspread.utils.rowcol_to_a1(k, TASK_HEADER.index('status') + 1)
        gf.format_cell_range(worksheet, cell_in_worksheet, fmt)


def sort_tasks_by_datetime(worksheet:gspread.worksheet.Worksheet) -> bool:
    '''
    Sorts the user task by due date, with the earliest date at the top.

    Arguments:
    - worksheet:gspread.worksheet.Worksheet ---> user worksheet connection

    Returns a bool.
    '''
    due_date_col, _ = get_column(worksheet = worksheet,
                                    column_name = 'due',
                                    header = TASK_HEADER)
    due_dates_tasks = [datetime.strptime(d, "%m-%d-%Y").date() for d in due_date_col[1:]]
    due_dates_tasks_ordered = sorted(due_dates_tasks)
    due_date_idx = [due_dates_tasks.index(d) for d in due_dates_tasks_ordered]
    overdue_task_row = [i + 2 for i in range(len(due_dates_tasks_ordered)) \
                        if due_dates_tasks_ordered[i] < datetime.now().date()]
    
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
    '''
    Retrievs and validates the indexes of that tasks to be removed from the task list.
    
    Arguments:
    - tasks_idx:list[int] ---> a list with the indexes of the tasks to be removed.

    Returns a bool.
    '''
    
    
    while True:
        
        task_remove_idx = input('Please enter the indexes for tasks to be removed.\n'
                            'Use commas to separate multiple entries.\n'
                            '(Enter Exit to cancel): \n')
        
        # Smooth application exit:
        smooth_exit(task_remove_idx)

        task_remove_idx = task_remove_idx.split(',')
            
        if sum([True for k in task_remove_idx if k in tasks_idx]) == len(task_remove_idx):
            break
        
        if len(tasks_idx) == 0:
            print('There are no tasks to remove!')
            return False
    
    return task_remove_idx


def delete_task(user_data:dict, worksheet:gspread.worksheet.Worksheet, user_task_data:dict) -> None:
    '''
    Deletes one or more tasks by removing the corresponding rows from the user worksheet.
    The task IDs separated by commas are entered by the user. After input validation, the task deletion
    awaits for confirmation (yes or no) in order to proceed. After completion, the user returns to the main menu.
    
    Arguments:
    - user_data:dict ---> dictionary with user the information from the 'users'-worksheet
        - keys: user_id, user_name, email, password, and tasks
        - values:str

    - worksheet:gspread.worksheet.Worksheet ---> connection to user task worksheet 
    - user_task_data ---> dictionary with the user task information 
        - keys:str ---> task_id, description, created, due, and status
        - values:
            - task_id:str ---> task id
            - description:str ---> task description
            - created:datetime ---> creation date
            - due:datetime ---> due date
            - status:str ----> task status (active/overdue)

    delete_task(kwargs['user_data'], tasks, task_info)
    '''

    if int(user_data['tasks']) == 0:
        print('There are no tasks to remove!')

    else:
        # Check that user input task index corresponds with the task indexes from the worksheet:
        task_remove_idx = validate_task_index(user_task_data['task_id'])

        # Confirm the choice:
        remove_choice = input(f'You selected task {task_remove_idx} to be removed.'
                                'Press Yes(y) to proceed, No(n) to cancel: \n')
        
        # If the user inputs are valid, delete task(s) and update the remaining task_id cells 
        # to start from 1: 
        if validate_static_options(remove_choice, STATIC_OPTIONS):
            if remove_choice.lower() == 'y':
                task_remove_idx = sorted(list(set([int(k) for k in task_remove_idx])))
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
                taskid_col, column_id = get_column(worksheet = worksheet, 
                                                    column_name = 'task_id',
                                                    header = TASK_HEADER) 
                
                if len(taskid_col[1:]) == 0: # No more tasks left:
                    print('All task were removed!')
                    
                    # Update the cell containing the # of tasks in the user row form the 'user'-worksheet:
                    SHEET.worksheet(USERS).update_cell(int(user_data['user_id'])+1, 
                                        USER_HEADER.index('tasks') + 1,
                                        str(len(taskid_col[1:])))
                    return # Exit here, no need to continue 
                
                ## If there are more tasks left, make sure they are sorted ascending by due date and 
                ## get the task id column info: 
                if sort_tasks_by_datetime(worksheet):
                    taskid_col, column_id = get_column(worksheet = worksheet,
                                                        column_name = 'task_id',
                                                        header = TASK_HEADER)

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


def delete_account(**kwargs) -> bool:
    '''
    Deletes the user account in the following order:
    - removes the user info from the 'users'-worksheet
    - updates the 'user_id' column from the 'users'-worksheet
    - removes the worksheet containing the user tasks
    
    Arguments:
    - users_worksheet_name:str
    - user_name:str
    - user_column_name:str
    - user_id_column_name:str 
    - header:str

    Returns a bool. 

    user_name:str, worksheet:gspread.worksheet.Worksheet

    '''

    remove_choice = input('Your account will be deleted. \n'
                            'Press Yes(y) to proceed, No(n) to cancel: \n')
    
    if validate_static_options(remove_choice, STATIC_OPTIONS):
        if remove_choice.lower() == 'y':

            users_worksheet = SHEET.worksheet(kwargs['users_worksheet_name'])
            user_worksheet  = SHEET.worksheet(kwargs['user_name'])

            # Remove the row containing the user information from the 'users'-worksheet:
            user_data = get_user_info(worksheet = users_worksheet,
                                        column_name = kwargs['user_column_name'],
                                        user_name = kwargs['user_name'],
                                        header =  kwargs['header'])

            user_column, _ = get_column(worksheet = users_worksheet,
                                        column_name = 'user_column_name',
                                        header = kwargs['header'])
            _, row_index = get_row(worksheet = users_worksheet, 
                                    worksheet_column_data = user_column,
                                    user_name =  user_data['user_name'])
            SHEET.worksheet(kwargs['user_worksheet_name']).delete_rows(row_index)

            # Update the 'user_id'-column from the 'users'-worksheet:
            user_id_column, column_idx = get_column(worksheet = users_worksheet,
                                                    column_name = kwargs['user_id_column_name'],
                                                    header = kwargs['header'])
            user_id_column[1:] = [i + 1 for i in range(len(user_id_column[1:]))]

            for i in range(len(user_id_column[1:])):
                users_worksheet.update_cell(i + 2, column_idx, user_id_column[i + 1])

            # Remove the user worksheet:
            SHEET.del_worksheet(user_worksheet)

            print('The account was deleted!')
            return True

        else:
            print('Operation cancelled.')
            return False 


def validate_new_task_description() -> list[str]:
    '''
    Validates the task description entry. 
    The task description must be non-empty and have maximum 44 characters.
    
    Returns a list containing the new task definition:
        - task_id:str ---> task id
        - description:str ---> task description
        - created:datetime ---> creation date
        - due:datetime ---> due date
        - status:str ----> task status (active)
    '''
    while True:
        
        new_task = input('Enter a new task (maximum 44 characters): \n')
        
        # Smooth application exit:
        smooth_exit(new_task)

        if len(new_task) == 0 :
            print('A new task cannot be empty. Please try again.')
        elif len(new_task) > 44:
            print(f'The task contains {len(new_task) - 44} extra characters. Please try again.')
        else:
            break
        
    return new_task


def validate_due_date() -> datetime:
    '''
    Checks if the datetime input provides the valid day, month and year values in the 
    requested format MM-DD-YYY (e.g., 05-15-2024), otherwise it throws a ValueError.
    The due date also has to be past the current time.

    Returns a tupple containing the string formatted creation and due dates.  
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


def add_task(**kwargs) -> dict:
    '''
    Add a new task to the user worksheet. The new task is inserted such that 
    it maintains the default sorting by due date, with the earliest due date at the top.

    Arguments:
    - users_worksheet_name:str
    - user_data:dict
    - header:str

    add_task(users_worksheet_name = USERS, user_data = user_data, header = TASK_HEADER)

    Returns a dictionary containing the newly added task:
    - keys:str - 'task_id', 'description', 'created', 'due', 'status'
    - values:list[str]  
    '''

    #users_worksheet = SHEET.worksheet(kwargs['users_worksheet_name'])
    #user_worksheet  = SHEET.worksheet(kwargs['user_name'])

    #_, task_row = tasks_list(user_data)
    # user_data = get_user_info(worksheet = users_worksheet,
    #                     column_name =  kwargs['user_column_name'], 
    #                     user_name = kwargs['user_name'],
    #                     header =  kwargs['header'])

    #user_data = get_user_info(USERS, user_data['user_name'])

    task_row = dict.fromkeys(kwargs['header']) #TASK_HEADER
    task_row['description'] = validate_new_task_description()
    task_row['due'], task_row['created'] = validate_due_date()
    task_row['status'] = 'active'
    task_row['task_id'] = str(int(kwargs['user_data']['tasks']) + 1)
    task_info = list(task_row.values())
    
    
    user_worksheet = SHEET.worksheet(kwargs['user_data']['user_name'])
    user_worksheet.append_row(task_info)
    
    # Keep the tasks sorted ascedning by due date.
    # If not sorted, then sort and update the task indexes. 
    if sort_tasks_by_datetime(user_worksheet): 
        taskid_col, column_id = get_column(worksheet = user_worksheet,
                                            column_name = 'task_id',
                                            header = TASK_HEADER)
        for k in range(len(taskid_col[1:])):    
            SHEET.worksheet(kwargs['user_data']['user_name']).update_cell(k + 2, column_id, k+1)


    # Update the  number of tasks in the 'tasks' column from the 'users'-worksheet:
    users_worksheet = SHEET.worksheet(kwargs['users_worksheet_name'])
    user_column, _ = get_column(worksheet = users_worksheet, #USERS
                                column_name = 'user_name',
                                header = USER_HEADER)
    user_row, row_index = get_row(worksheet = users_worksheet,  #USERS
                                    worksheet_column_data = user_column,
                                    user_name = kwargs['user_data']['user_name'])
    user_row = dict(zip(USER_HEADER, user_row))
    user_row['tasks'] = str(int(user_row['tasks']) + 1)

    # Update user row:
    _, column_index = get_column(worksheet = users_worksheet, #USERS
                                column_name = 'tasks', 
                                header = USER_HEADER)
    users_worksheet.update_cell(row_index, column_index, int(user_row['tasks']))

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
                'Valid options: 1 (User Login), 2 (Register User), 3 (Help), 4 (Exit): \n')
        elif input_option.isdigit() and int(input_option) not in range(1, 5):
            print('Invalid choice!\n'
                'Valid options: 1 (User Login), 2 (Register User), 3 (Help), 4 (Exit): \n')
        else:
            break

    return int(input_option)


def handle_input_options(**kwargs) -> None:
    '''
    Takes the menu selection from user input and handles the menu item logic:
    - 1 : User Login
    - 2 : Register a new user
    - 3 : Show the help content for running the application
    - 4 : Exit the application

    Arguments:
    - input_option:int
    - users_worksheet_name
    - user_header
    - task_header

    '''
    while True:
        if kwargs['input_option'] == 1: # USER LOGIN

            user_data = user_login(worksheet_name = kwargs['users_worksheet_name'],
                                    user_column_name = kwargs['user_column_name'],
                                    password_column_name = kwargs['user_password_name'],
                                    header = kwargs['user_header'])
                
            task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                        user_column_name = kwargs['user_column_name'],
                        user_data = user_data,
                        user_header = kwargs['user_header'],
                        task_header = kwargs['task_header']) 
            break
        elif kwargs['input_option'] == 2: # REGISTER NEW USER
            user_data = new_user_registration()
            task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                        user_column_name = kwargs['user_column_name'],
                        user_data = user_data,
                        user_header = kwargs['user_header'],
                        task_header = kwargs['task_header']) 
            break
        elif kwargs['input_option'] == 3: # HELP MENU
            clear_output('y')
            user_help()
            clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise.\n'
                            '(Enter Exit to cancel): \n'))

            handle_input_options(input_option = main_menu(), 
                                users_worksheet_name = kwargs['users_worksheet_name'],
                                user_column_name = kwargs['user_column_name'],
                                user_password_name = kwargs['user_password_name'],
                                user_header = kwargs['user_header'],
                                task_header =  kwargs['task_header'])
        else: # Exit app
            print('You are now logged out.\n')
            sys.exit(0)

def task_handler(**kwargs) -> None:
    '''
    task_handler(user_data:dict)

    Handles the menu options for registered users:
    - 1 (View tasks):     ---> List all tasks
    - 2 (Add task):       ---> Add a new task
    - 3 (Delete task):    ---> Delete a task
    - 4 (Delete account): ---> Delete user account
    - 5 (Exit):           ---> Return to the main menu

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
                tasks, task_info = tasks_list(kwargs['user_data'], kwargs['task_header'])
                if int(kwargs['user_data']['tasks']) == 0:
                        print('You have no scheduled tasks.\n')
                        clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))
                        task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                                user_column_name = kwargs['user_column_name'],
                                user_data = kwargs['user_data'],
                                user_header = kwargs['user_header'],
                                task_header = kwargs['task_header'])
        
                else:
                    print('Your tasks are listed below:')
                    print(tabulate(task_info, headers="keys", numalign="center"))
                    clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))
                    task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                                user_data = kwargs['user_data'],
                                user_column_name = kwargs['user_column_name'],
                                user_header = kwargs['user_header'],
                                task_header = kwargs['task_header'])
                    
            elif user_choice == 2: # Add a new ask
                add_task(users_worksheet_name = kwargs['users_worksheet_name'], 
                            user_data = kwargs['user_data'],
                            header = kwargs['task_header']) #TASK_HEADER
                user_data = get_user_info(worksheet = kwargs['users_worksheet_name'],
                                            column_name = kwargs['user_column_name'], 
                                            user_name = kwargs['user_data']['user_name'],
                                            header = kwargs['user_header'])
                task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                                user_column_name = kwargs['user_column_name'],
                                user_data = user_data,
                                user_header = kwargs['user_header'],
                                task_header = kwargs['task_header'])

            elif user_choice == 3: # Delete task
                tasks, task_info = tasks_list(kwargs['user_data'], kwargs['task_header'])
                print('Your tasks are listed below:')
                print(tabulate(task_info, headers="keys", numalign="center"))
                delete_task(kwargs['user_data'], tasks, task_info)
                clear_output(input('\nPress y (Yes) to clear the output, or n (No) otherwise: \n'))

                user_data = get_user_info(worksheet = kwargs['users_worksheet_name'],
                                            column_name = kwargs['user_column_name'], 
                                            user_name = kwargs['user_data']['user_name'],
                                            header = kwargs['user_header'])
                task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                                user_column_name = kwargs['user_column_name'],
                                user_data = user_data,
                                user_header = kwargs['user_header'],
                                task_header = kwargs['task_header'])

                #task_handler(get_user_info(USERS, user_data['user_name']))
            
            elif user_choice == 4: # Delete user account
                account_deleted = delete_account(users_worksheet_name = kwargs['users_worksheet_name'],
                                                    user_name = kwargs['user_data']['user_name'],
                                                    user_column_name = 'user_name',
                                                    user_id_column_name = 'user_id', 
                                                    header = kwargs['user_header'])
                if account_deleted:
                    print('You are now logged out.\n')
                    sys.exit(0)
                else:
                    task_handler(users_worksheet_name = kwargs['users_worksheet_name'],
                                user_column_name = kwargs['user_column_name'],
                                user_data = kwargs['user_data'],
                                user_header = kwargs['user_header'],
                                task_header = kwargs['task_header'])
            else:
                print('You are now logged out.\n')
                sys.exit(0)


#%%                
# The main() function to run the app:
def main() -> None:
    '''
    The main() function to run the stack.
    '''

    print(  '*******************************************************************\n'
            '*** Welcome to LovePlanning, the Ultimate Task Management Tool! ***\n'
            '*******************************************************************\n')

    while True:
        # Try-except block at the top of the call stack to handle API call errors
        # and exit gracioulsy if that happens: 
        try:
            input_option = main_menu() 
            # Hard-coded inputs here:
            if not  handle_input_options(input_option = input_option, 
                                            users_worksheet_name = USERS,
                                            user_column_name = 'user_name',
                                            user_password_name = 'password',
                                            user_header = USER_HEADER,
                                            task_header =  TASK_HEADER):
                print('You are now logged out.\n')
                break
        except gspread.exceptions.APIError as e:
            print(f' An API error has occured: {e}.\n'
                'Exiting application....')
            sys.exit(1) 

# %%

# Run the App:

main()

