
#=================================================================#
# Write your code to expect a terminal of 80 characters wide and 24 rows high
#=================================================================#

import gspread
from google.oauth2.service_account import Credentials
import regex as re
from tabulate import tabulate
import pprint
import os
#import pandas as pd
from dataclasses import dataclass, field
from typing import List

from datetime import datetime
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
TASK_HEADER = ['user_id', 'task_id', 'description', 'category', 'created', 'due', 'status']
TASK_CATEGORY = ['errand', 'personal', 'work']

# @dataclass
# class Defaults:
#     USERS: str = 'users'
#     TASKS: str = 'tasks'
#     #STATIC_OPTIONS: list['str'] = field(['y', 'n'])
#     USER_HEADER:list = field(default=['user_id','user_name','email','password'])
    

#=================================================================#
# --------------------- For New Users: ---------------------------#
#----------------------------------------------------------------#
'''
New users:
- input user_name
    - validate user_name
        - non-empty
        
- input password

'''

#----------------------------------------------------------------#

def clean_cli() -> None:
# https://www.geeksforgeeks.org/clear-screen-python/
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
def clear_output(clean_cli_choice:str) -> None:
    if validate_static_options(clean_cli_choice, STATIC_OPTIONS):
        clean_cli()
def make_dict_from_nested_lists(list_data:list[list], d_keys:list[str]) -> dict:
    '''
    Takes the google sheet data as list of lists and creats a dictionary using 
    dictionary comprehension. The keys are the values in the first list (list_data[0]) of the list_data entry.
    Each dictionary key receives a list of values from the remaining lists of list_data argument. 
    Handy for printing the user data or for handling data inputs (though with care when there are 
    many regsitered users)        
    '''

    #task_info.insert(0,task_header[1:])
    #d_keys = list_data[0]

    list_data.copy().insert(0, d_keys) # shallow list copy to avoid changing the original variable 

    return {d_keys[i]:[s[i] for s in list_data] for i in range(len(d_keys)) }  

def validate_password_length(user_password:str):
    '''
    Validate entry password for new users: 
    password must contain at least 8 characters.
    '''

    try: 
        if len(user_password) <= 8:
            raise ValueError(
                    f'At least 8 characters required, you provided {len(user_password)}'
                )
        else:
            return True 
    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n')
        return False

def validate_user_password_capital(user_password:str):
    '''
    Validate entry password for new users: 
    password must contain at least one capital letter. 
    '''
    capital_letters = [s for s in user_password if s.isupper()]

    try:
        if len(capital_letters) < 1:
            raise ValueError(
                    f'At least one capital letter required, you provided {len(capital_letters)}'
                )
        else:
            return True
    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n')
        return False

def validate_user_password_numerals(user_password:str):
    '''
    Validate entry password for new users.
    The password must contain at least two numerals.
    '''          
    
    try:
        is_num_in_str = re.match(r'[0-9]', user_password) is not None
        if is_num_in_str:
            num_in_str = re.match(r'[0-9]', user_password).span() 
            if len(num_in_str) <=2:
                raise ValueError(
                    f'At teast two numerals are required, you provided {len(num_in_str)}'
                    )
            else:
                return True 
    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n') 
        return False


def validate_user_password(**kwargs):
    '''
    Validate entry password for new users: at least 8 characters length, of which
    at least one capital letter and at least two numerals.
    '''
        
    while True:
        
        new_user_password = input('Please enter your pasword: ')
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

def validate_username() -> bool:
    '''
    Validate the user input for login option:
    - The name and passord strings must not be empty;
    - The input must contain two strings separated by comma;
    It applies to registered users, as well as to new users trying to register.
    '''
    username_column = get_column(SHEET.worksheet(USERS), 'user_name', USER_HEADER)
    while True:
        new_user_name = input('Please enter your username: ')
        try: 
            if len(new_user_name) == 0:
                raise ValueError('Username must not be empty')
            elif new_user_name in username_column[-1]:
                raise ValueError('Username not available')
            else:
                break
        except ValueError as e:
            print(f'Invalid username: {e}. Please try again!')
            return False
    
    return new_user_name

def validate_user_email() -> bool:
    '''
    Check if the string contains a valid email address 
    using regular expressions (regex).
    https://www.w3schools.com/python/python_regex.asp 
    '''
    
    valid_pattern = r"^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"

    while True:
        new_user_email = input('Please enter your email address: ')
        try: 
            if re.search(valid_pattern, new_user_email) is None:
                print('Condition 1 not met')
                raise ValueError(
                        f'Please enter a valid email address'
                    )
            else:
                break
        except ValueError as e:
            print(f'Invalid email address: {e}, please try again.\n')

    return new_user_email




def check_new_user_credentials(**kwargs) -> bool:
    '''
    Validates username and password for new users by matching them against the
    records of the rehistered users in the 'users' sheet. The new user credentials
    should not be found aming the credentials of the existing users. Passwords are not
    mached against the registered ones, since that would be a security break.
    Attributes:
    - user_name: string
    - user_email: string
    - password:string
    
    Returns a bool (True/False).  
    '''
    
    username_column = get_column(SHEET.worksheet(USERS), 'user_name', USER_HEADER)
    user_email_column = get_column(SHEET.worksheet(USERS), 'email', USER_HEADER)
    
    if (kwargs['user_name'] not in username_column[-1]) and \
        (kwargs['user_email'] not in user_email_column[-1]) :
        SHEET.add_worksheet(title = kwargs['user_name'], rows=1000, cols = len(TASK_HEADER))
        # Write the default worksheet column names:
        SHEET.worksheet(kwargs['user_name']).append_row(TASK_HEADER)
        new_user_data = [len(username_column) + 1, 
                        kwargs['user_name'],
                        kwargs['user_email'],
                        kwargs['password'],
                        kwargs['tasks']]
        SHEET.worksheet(USERS).append_row(new_user_data)
        #new_user_data = make_dict_from_nested_lists([new_user_data], USER_HEADER)
        new_user_data = dict(zip(USER_HEADER, new_user_data))
        return new_user_data
    else: 
        print('Username and password not available, please try again')
        return False

def new_user_registration():
    '''
    Validates credentials (username and password) from user input.
    - The while-loop runs until the user enters the correct data. 
    - Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data (without header)
    ''' 

    new_user_name = validate_username()
    new_user_password = validate_user_password(length=8,
                                            capital_letters=1,
                                            digits=2)
    new_user_email = validate_user_email()

    new_user_data = check_new_user_credentials(user_name = new_user_name,
                                                password = new_user_password,
                                                user_email = new_user_email,
                                                tasks = 0)
    
    
    print('Registration successful!\n')
            
    return new_user_data

#=================================================================#
# ------------------- For Registered Users: ----------------------#

def validate_login_input(user_input:str) -> bool:
    '''
    Check if the user log input contains two non-empty strings 
    (username and passord) separated by comma. 
    '''
    
    try:
        if len(user_input) == 0:
            raise ValueError('Enter username and password separated by comma')
        elif user_input.find(',') < 0:
            raise ValueError('Use comma to separate username and password.')    
        else:
            user_input = user_input.split(',')
            if len(user_input[0]) == 0 and len(user_input[1]) == 0:
                raise ValueError('Username and Password cannot be empty.')
            elif len(user_input[0].strip()) == 0:
                raise ValueError('Username cannot be empty.')
            elif len(user_input[1].strip()) == 0:
                raise ValueError('Password cannot be empty.')
            else:
                return user_input
    except ValueError as e:
            print(f'{e}. Please try again!')
            return False

def match_user_name(user_data:dict, user_name:str) -> bool:
    '''
    Validates existing usernames by matching them against the
    records in the 'username'- column of the 'users'- sheet.  
    '''
 
    while True:
        if user_name in user_data['user_name']:
            return True
        else:
            print('Username not found, please try again')
            return False

def match_user_credentials(user_data:dict, user_name:str, user_password:str) -> bool:
    '''
    Validates existing username and passowrd by matching them against the
    user records in the 'users' sheet. Returns a bool (True/False)  
    '''
    while True:
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
    wksheet = SHEET.worksheet(worksheet_name)
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
    return col_data

def get_row_index(worksheet:gspread.worksheet.Worksheet, users_col:list[str], user_name:str) -> list:
     # Get the index of the username in the column
    user_idx = users_col.index(user_name)+1
    # Retrieve the row containig the user info based n the username index:
    user_info = worksheet.row_values(user_idx)
    return user_info

def get_user_info(sheet_name:str, user_name:str, column_name:str) -> dict:
    '''
    Get the user info from the 'users' worksheet based on 
    the username index. Can be handy when there are many 
    registered users since it does not require to import the 
    entire worksheet data. Notice that the for Google Sheets,
    the row numbers start at 1, while Python list indices start at 0.
    Returns a dictionary with the header values as keys and user records as values. 
    '''
    
    # Connect to the worksheet and retrive the header:
    users, user_header = get_sheet_meta(sheet_name)

    # Get the user index in the user_id column:
    #userame_col_idx = user_header.index(column_name) + 1
    
    # Get the usernames column from the worksheet indexed by userame_col_idx:
    #users_col = users.col_values(userame_col_idx)
    users_col = get_column(users, column_name, user_header)

    # Retrieve the row containig the user info based n the username index:
    user_info = get_row_index(users, users_col, user_name)

    return dict(zip(user_header, user_info))

def list_tasks_simple(user_data:dict) -> tuple[list[list[str]], list[str]]:
    '''
    Get the tasks by the user_id of a registered user.
    Returns the nested list of tasks (first return) and
    the header of the 'tasks' worksheet (second return).  
    '''

    tasks, task_header = get_sheet_meta(user_data['user_name'])
    # Get the data in the 'user_id' column
    userid_col = get_column(tasks, 'user_id', task_header)

    # Get all the row values for the tasks associated to an user_id:   
    tasks_idx = [i+1 for i in range(len(userid_col)) if userid_col[i] == user_data['user_id']]
    task_info = [tasks.row_values(int(t_ixd))[1:] for t_ixd in tasks_idx]
    #make_dict_from_nested_lists(task_info, task_header[1:])

    return tasks, task_info, task_header, tasks_idx

def user_login() -> list:
    '''
    Validates credentials (username and password) from user input.
    - The while-loop runs until the user enters the correct data. 
    - Returns the user data from the 'tasks'- google sheet as a dictionary
        - keys: column names (worksheet header)
        - values: column data (without header)
    '''
    while True:
        user_input = input('Please enter your username and password separated by comma: ')
        
        # Validate user_input: two strings separated by comma:
        user_input = validate_login_input(user_input)
        if user_input:
            # Retrieve the input components: username [0] and password [1]
            user_name = user_input[0].strip()
            user_password = user_input[1].strip()

            # Get the user data from the 'users' Google worksheet:
            try:
                user_data = get_user_info(USERS, user_name, 'user_name')
                if match_user_credentials(user_data, user_name, user_password):
                    print('Login successful!')
                    break
            except ValueError as e:
                print(f' {e}. Please try again.')
    
    return user_data
                    
def user_help() -> None:
    print('This is the help')
    return 

def validate_task_index(task_remove_idx:list[int], tasks_idx:list[int]) -> bool:
    while True:
        if all([True for k in task_remove_idx if k in  tasks_idx]):
            return True
        else:
            break
    return True
    
def validate_static_options(remove_choice:str, options:list[str]) -> bool:
    while True:
        if remove_choice.lower() not in options:
            remove_choice = input('Invalid option: please press y(Yes) to proceed, or n(No) to return: ')
        else:
            break
            
    return True
    
def delete_task(user_data:dict,
                #tasks:gspread.worksheet.Worksheet,
                #task_info:list[list[str]],
                #task_header:list[str]
                #tasks_idx:list[int]
                **kwargs) -> None:
    '''
    Delete one or more selected tasks by task id.
    The function removes the rows corresponding to the selected tasks from the 'tasks'Google worksheet.
    The task ids separated by commas are entered by the user.
    After input validation, the task deletion (yes or no) is completed according to the user choice.
    After completion, the user returns to the main menu.
    '''

    task_remove_idx = input('Please enter the indexes of the tasks to be removed or Escape to cancel.\n'
                            'Use commas to separate multiple entries: \n')
    
    # Check that user input task index corresponds with the task indexes from the worksheet:
    if validate_task_index(task_remove_idx, kwargs['tasks_idx']):
        remove_choice = input(f'You selected task {task_remove_idx} to be removed.\n'
                            'Press Yes(y) to proceed, No(n) to return or Escape to cancel: ')
    
    # If the user inputs are valid, delete task(s) and update the remaining task_id cells 
    # to start from 1: 
    if validate_static_options(remove_choice, STATIC_OPTIONS):
        if remove_choice.lower() == 'y':
            task_remove_idx = sorted(list(set([int(k) for k in task_remove_idx.split(',')])))
            user_task_data = make_dict_from_nested_lists(kwargs['task_info'], kwargs['task_header'][1:])
            user_task_data['task_id'] = [int(i) for i in  user_task_data['task_id'] ]

            # Subset the worksheet rows to be deleted: 
            user_row_remove_idx = [user_task_data['task_id'].index(i) for i in user_task_data['task_id'] \
                                    if i in task_remove_idx]

            # Update the worksheet:
            ## Delete one row (task) at a time:      
            reduce_idx = 0
            for k in user_row_remove_idx:
                row_to_delete = [kwargs['tasks_idx'][i] - reduce_idx for i in user_row_remove_idx if i == k]
                kwargs['tasks'].delete_rows(row_to_delete[0])
                print(f'Task {k} deleted...Row {row_to_delete[0]} deleted.')
                reduce_idx += 1
            
            ## Update task index: 
            ### Get the row and column ids for the user: 
            userid_col = get_column(kwargs['tasks'], 'user_id', kwargs['task_header'])   
            user_row_idx = [i+1  for i in range(len(userid_col)) if userid_col[i] == user_data['user_id']] 
            #taskid_col = get_column(kwargs['tasks'], 'task_id', kwargs['task_header'])
            taskid_col = list(user_task_data.keys()).index('task_id') + 2
        
            update_idx = 1
            for k in user_row_idx:    
                kwargs['tasks'].update_cell(k, taskid_col, update_idx)
                update_idx += 1
    
            # Check if there any task left:

            ## ERRORS HERE:   
            for k in list(user_task_data.keys()):
                del user_task_data[k][task_remove_idx]
            
            if (len(user_task_data['task_id'])==0):
                print('There is no active task left in the list!')
            else:
                #
                print(f"{len(user_row_remove_idx)} tasks deleted, {len(user_task_data['task_id'])} remaining.")
                #user_task_data['task_id'] = [i+1 for i in range(len(user_task_data['task_id']))]

    else:
        print('Operation cancelled.')     

def validate_new_task_description() -> list[str]:
    '''
    Validates the task description entry. 
    The task description must be non-empty and
    have at most 70 characters. 
    '''
    while True:
        
        new_task = input('Enter a new task (maximum 70 characters): ')

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
        task_category = input('Specify the task category (errand, personal, or work): ')
        if str(task_category).lower().strip() not in TASK_CATEGORY:
            print('Invalid choice. Please select a valid category (errand, personal, or work): ')
        else:
            break       
    
    return task_category
        
def validate_due_date() -> datetime:
    '''
    Checks if the datetime input provides the valid day, month and year values in the 
    requested format MM-DD-YYY (e.g., 15-05-2024), otherwise it throws a ValueError.
    '''
    #due_date = due_date.split('-')
    #due_date = [d.lstrip('0') for d in due_date]

    while True:
        due_date = input('Enter the due date for the task in the MM-DD-YYYY format: ')
        try:
            due_date = datetime.strptime(due_date, "%m-%d-%Y")
            #doy = due_date[0]
            #moy = due_date[1]
            #yr  = due_date[2]
            break
        except ValueError as e:
            print('Invalid format. Please enter the date as MM-DD-YYYY.')
            
    return due_date

def create_new_task() -> dict:
    '''
    Add a new task to the user worksheet. The new task is inserted such that 
    it maintains the default sorting by due date, with the earliest due date at the top. 
    '''
        
    new_task = validate_new_task_description()
    print('New task added.')
    task_category = validate_new_task_category()
    print(f'Task category {task_category.upper()} added.')
    due_date = validate_due_date()
    print(f'Task due date {due_date} added.')   
    task_info = [new_task, task_category,'chore', due_date, 'active']

    #user_id
    #task_id 

    # SHEET.add_worksheet(title = kwargs['user_name'], rows=1000, cols = len(TASK_HEADER))
    # # Write the default worksheet column names:
    # SHEET.worksheet(kwargs['user_name']).append_row(TASK_HEADER)
    # new_user_data = [len(username_column) + 1, 
    #                 kwargs['user_name'],
    #                 kwargs['user_email'],
    #                 kwargs['password'],
    #                 kwargs['tasks']]
    # SHEET.worksheet(USERS).append_row(new_user_data)



    return dict(zip(TASK_HEADER, task_info))

def main_menu() -> None:
    '''
    Gets input data to register a new user. 
    Run a while loop to collect a valid string of data
    from the user via the terminal. The loop will repeatedly
    request user input data, until it is valid. 
    '''
    #print('Select an option: 1(Login), 2(Register), 3(Remove user), 4(Help), 5(Exit):')

    while True:
        input_option = int(input('Select an option: 1(Login), 2(Register), 3(Remove user), 4(Help), 5(Exit): '))
        if(input_option not in range(1, 5)):
            print('Invalid choice!\n'
                  'Enter a valid option: 1(Login), 2(Register), 3(Remove user), 4(Help), 5(Exit):')
        else:
            break
    return input_option

def handle_input_options(input_option:int) -> None:
    '''
    Takes the menu selection from user input and handles the menu item logic.  
    '''
    while True:
        if input_option == 1:
            user_data = user_login()
            task_handler(user_data)  # takes user_id and returns the user tasks
            break
        elif input_option == 2: # Regiister new user
            user_data = new_user_registration()
            task_handler(user_data) 
            break
        elif input_option == 3:
            user_help()
            break
        else:
            break

def task_handler(user_data:dict) -> None:
    '''
    List and handles the available options for registered users:\n
    '1 (View), 2 (Add), 3 (Delete), 4 (Exit)'
    '''
    print(' Please enter an option: 1 (View), 2 (Add), 3 (Delete), 4 (Exit): ')

    while True:
        user_choice = int(input())
        if(user_choice not in range(1, 5)):
            print('Please enter a valid option: 1 (View), 2 (Add), 3 (Delete), 4 (Exit).\n'
                'Press Escape(Esc) to Cancel.')
        else:
            if user_choice != 4:
                tasks, task_info, task_header, tasks_idx = list_tasks_simple(user_data)
                #print('User tasks retrieved.\n')
            else:
                break # Exit the outer if-else

            if user_choice == 1: # View tasks
                if len(task_info) == 0:
                        print('You have no scheduled tasks.')
                else:
                    print('Your tasks are listed below:')
                    # Formatted user tasks console print
                    print(tabulate(task_info, headers = task_header[1:]))
                    clean_cli = input('Press y(Yes) to clear the output, or n(No) otherwise: ')
                    clear_output(clean_cli)
                    task_handler(user_data)
                #break
            elif user_choice == 2: # Add ask
                create_new_task()
                task_handler(user_data)
            elif user_choice == 3: # Delete task
                print('Your tasks are listed below:')
                # Formatted user tasks console print
                print(tabulate(task_info, headers = task_header[1:]))
                delete_task(user_data = user_data,
                            tasks = tasks,
                            task_info = task_info,
                            task_header = task_header,
                            tasks_idx = tasks_idx)
                clean_cli = input('Press y(Yes) to clear the output, or n(No) otherwise: ')
                clear_output(clean_cli)
                task_handler(user_data)  
            else:
                return False
                
#=================================================================#
# -------------- Run the App: ---------------------------#

def main() -> None:
    print('Welcome to LovePlanning, the Ultimate Task Management Tool!')
    input_option = main_menu()
    while True:
        if not handle_input_options(input_option):
            print('You are now logged out')
            break

main()