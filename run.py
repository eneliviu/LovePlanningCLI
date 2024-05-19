
#=================================================================#
# Write your code to expect a terminal of 80 characters wide and 24 rows high
#=================================================================#

import gspread
from google.oauth2.service_account import Credentials
import regex as re
from tabulate import tabulate
import pprint
import os

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
#=================================================================#
# --------------------- For New Users: ---------------------------#


def clean_cli() -> None:
# https://www.geeksforgeeks.org/clear-screen-python/
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def clear_output(clean_cli_choice:str) -> None:
    if validate_static_options(clean_cli_choice, STATIC_OPTIONS):
        clean_cli()


def validate_password_length(user_data:str):
    '''
    Validate entry password for new users: 
    password must contain at least 8 characters.
    '''
    try: 
        if len(user_data) <= 8:
            raise ValueError(
                    f'At least 8 characters required, you provided {len(user_data)}'
                )
    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n')
        return False

    return True 
def validate_user_password_capital(user_data:str):
    '''
    Validate entry password for new users: 
    password must contain at least one capital letter. 
    '''
    print(f'You entered: {user_data}')
  
    capital_letters = [s for s in user_data if s.isupper()]

    try:
        if len(capital_letters) <2:
            raise ValueError(
                    f'At least one capital letter required, you provided {len(capital_letters)}'
                )

    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n')
        return False
    
    return True
def validate_user_password_numerals(user_data:str):
    '''
    Validate entry password for new users: 
    password must contain at least two numerals.
    '''          
    num_in_str = re.match(r'[0-9]', user_data).span()
        
    try:
        if len(num_in_str) <=2:
            raise ValueError(
                f'Al teast two numerals are reuqired, you provided {len(num_in_str)}'
                )
    except ValueError as e:
        print(f'Invalid password: {e}, please try again.\n') 
        return False      
             
    return True  
def validate_user_email(user_data:str):
    '''
    Check if the string contains a valid email address 
    using regular expressions (regex).
    https://www.w3schools.com/python/python_regex.asp 
    '''
    print(f'You entered: {user_data}')
    valid_pattern = r"^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
    try: 
        if re.search(valid_pattern, user_data) is None:
            raise ValueError(
                    f'Please enter a valid email address'
                )
    except ValueError as e:
        print(f'Invalid email address: {e}, please try again.\n')
        return False

    return False
def user_register():
    user_name = input('Please enter your username: ')
    validate_username(user_name)
    
    user_password = input('Please enter your pasword: ')
    validate_password_length(user_password)
    validate_user_password_capital(user_password)
    validate_user_password_numerals(user_password)

    user_email = input('Please enter your pasword: ')
    validate_user_email(user_email)

def make_dict_from_nested_lists(list_data:list[list]) -> dict:
    '''
    Takes the google sheet data as list of lists and creats a dictionary using 
    dictionary comprehension. The keys are the values in the first list (list_data[0]) of the list_data entry.
    Each dictionary key receives a list of values from the remaining lists of list_data argument. 
    Handy for printing the user data or for handling data inputs (though with care when there are 
    many regsitered users)        
    '''
    d_keys = list_data[0]
    return {d_keys[i]:[s[i] for s in list_data[1:]] for i in range(len(d_keys)) }  

#=================================================================#
# ------------------- For Registered Users: ----------------------#

def validate_login_input(user_input:str) -> bool:
    '''
    Check if the user name and passord login input contains
    two non-empty strings separated by comma. 
    '''

    try:
        if len(user_input[0]) < 4:
            raise ValueError('Please enter a valid username')
    except ValueError as e:
        print(f'')

    return True

def validate_username(user_name:str) -> bool:
    '''
    Validate the user input for login option:
    - The name and passord strings must not be empty;
    - The input must contain two strings separated by comma;
    It applies to registered users, as well as to new users trying to register.
    '''
    try: 
        if len(user_name) < 4:
            raise ValueError('Username should not contain at least four characters')
    except ValueError as e:
        print(f'Invalid username: {e}, please try again.\n')
        return False
    
    return True

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
            return False
        else:
            return False

def get_sheet_meta(worksheet_name:str) -> list:
    users = SHEET.worksheet(worksheet_name)
    users_header = users.row_values(1)
    return users, users_header

def get_user_column(worksheet:gspread.worksheet.Worksheet, column_name:str, header:list[str]) -> list[str]:
    '''
    Get the user_id column from a worksheet. Returns a list containing the column header and the values.
    Notice that the for Google Sheets, the row numbers start at 1, while Python list indices start at 0.
    Returns a dictionary with the header values as keys and user records as values.  
    '''
    # Get the 1-based index of the 'user_id' columns
    userid_col_idx = header.index(column_name) + 1
    # Get the data in the 'user_id' column
    userid_col = worksheet.col_values(userid_col_idx)
    return userid_col

def get_username_index(worksheet:gspread.worksheet.Worksheet, users_col:list[str], user_name:str) -> list:
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
    users_col = get_user_column(users, column_name, user_header)

    # Retrieve the row containig the user info based n the username index:
    user_info = get_username_index(users, users_col, user_name)

    return dict(zip(user_header, user_info))

def list_tasks_simple(user_data:dict, worksheet_name:str) -> tuple[list[int], list[list[str]]]:
    '''
    Get the tasks by the user_id of a registered user.
    Returns the nested list of tasks (first return) and
    the header of the 'tasks' worksheet (second return).  
    '''
    tasks, task_header = get_sheet_meta(worksheet_name)

    # Get the data in the 'user_id' column
    userid_col = get_user_column(tasks, 'user_id', task_header)

    # Get all the row values for the tasks associated to an user_id:   
    tasks_idx = [i+1 for i in range(len(userid_col)) if userid_col[i] == user_data['user_id']]
    task_info = [tasks.row_values(int(t_ixd))[1:] for t_ixd in tasks_idx]
    
    return task_info, task_header

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
        if validate_login_input(user_input):
            # Retrieve the input components: username [0] and password [1]
            user_input = user_input.split(',')
            user_name = user_input[0].strip()
            user_password = user_input[1].strip()

            # Get the user data from the 'users' Google worksheet:
            user_data = get_user_info(USERS, user_name, 'user_name')
            if match_user_credentials(user_data, user_name, user_password):
                print('Login successful!\n')
                
                break

    return user_data

def user_help() -> None:
    print('This is the help')
    return 

def validate_static_options(remove_choice:str, options:list[str]) -> bool:
    while True:
        if remove_choice.lower() not in options:
            remove_choice = input('Invalid option: please press y(Yes) to proceed, or n(No) to return: ')
        else:
            break
            
    return True
    
def delete_task(user_data:dict) -> None:
    '''
    Delete one or more selected tasks by task id.
    The function removes the rows corresponding to the selected tasks from the 'tasks'Google worksheet.
    The task ids separated by commas are entered by the user.
    After input validation, the task deletion (yes or no) is completed according to the user choice.
    After completion, the user returns to the main menu.
    '''
    task_remove_idx = input('Please enter the indexes of the tasks to be removed.'
                            'Use commas to separate multiple entries: \n')
    remove_choice = input(f'You selected task {task_remove_idx} to be removed.\n'
                            'Press Yes(y) to proceed, or No(n) to return: ')
    
    if validate_static_options(remove_choice, STATIC_OPTIONS):
  
        task_remove_idx = [int(k) for k in task_remove_idx.split(',')]
        
        if remove_choice.lower() == 'y':
            task_remove_idx = int(task_remove_idx)
            tasks, task_header = get_sheet_meta(TASKS)
            userid_col = get_user_column(tasks, 'user_id', task_header)           
            row_idx = [i  for i in range(len(userid_col)) if userid_col[i] == user_data['user_id']]
    
            row_idx = [row_idx[task_remove_idx]]
            
            # Check that user input task index corresponds with the task indexes from the worksheet:

            def validate_task_index(task_remove_idx:list[int], row_idx:list[int]):
                if all([True for k in task_remove_idx if k in  row_idx]):
                    return True
                else:


            for k in task_remove_idx:
                tasks.delete_rows(task_idx[k])
            print(f'Task {task_remove_idx - 1} deleted.')

            # Update the task_id for the remaining tasks:


        else:
            print('Operation cancelled.')  
    

def main_menu_options() -> None:
    '''
    Gets input data to register a new user. 
    Run a while loop to collect a valid string of data
    from the user via the terminal. The loop will repeatedly
    request user input data, until it is valid. 
    '''
    print('Please select an option: 1 (Log in), 2 (Register), 3 (Help) or 4 (Exit):')

    while True:
        input_option = int(input('Enter your choice: '))
        if(input_option not in range(1, 5)):
            print('Please enter a valid option: 1 (Log in), 2 (Register), 3 (Help) or 4 (Exit):')
        else:
            break
    return input_option

def handle_input_options(input_option:int) -> None:
    '''
    Takes the menu selection from user input and handles the menu item logic.  
    '''
    while True:
        if input_option == 1:
            user_data = user_login() # validates and returns credentials for regsistered users
            task_handler(user_data)  # takes user_id and returns the user tasks
            break
        elif input_option == 2:
            user_register()
            break
        elif input_option == 3:
            user_help()
            break
        else:
            return False

def add_new_task():
    pass

def task_handler(user_data:dict) -> None:
    '''
    List and handles the available options for registered users:\n
    '1 (View), 2 (Add), 3 (Delete), 4 (Exit)'
    '''
    print(' Please enter an option: 1 (View), 2 (Add), 3 (Delete), 4 (Exit): ')

    while True:
        user_choice = int(input())
        if(user_choice not in range(1, 5)):
            print('Please enter a valid option: 1 (View), 2 (Add), 3 (Delete), 4 (Exit)')
        else:
            if user_choice != 4:
                task_info, task_header = list_tasks_simple(user_data, TASKS)
                print('User tasks retrieved.\n')
            else:
                break # Exit the outer if-else

            if user_choice == 1: # View tasks
                if len(task_info) == 0:
                        print('You have no scheduled tasks.')
                else:
                    print('Your tasks are listed below:')
                    # Formatted user tasks console print
                    print(tabulate(task_info, headers = task_header[1:]))
                    clean_cli_choice = input('Press y(Yes) to clear the output, or n(No) otherwise: ')
                    clear_output(clean_cli_choice)
                    task_handler(user_data)
                #break
            elif user_choice == 2: # Add ask
                add_new_task()
            elif user_choice == 3: # Delete task
                print('Your tasks are listed below:')
                # Formatted user tasks console print
                print(tabulate(task_info, headers = task_header[1:]))
                delete_task(user_data)
                clean_cli_choice = input('Press y(Yes) to clear the output, or n(No) otherwise: ')
                clear_output(clean_cli_choice)
                task_handler(user_data)  
            else:
                return False
                

#=================================================================#
# -------------- Run the App: ---------------------------#

def main() -> None:
    print('Welcome to LovePlanning, the Ultimate Task Management Tool!')
    input_option = main_menu_options()
    while True:
        if not handle_input_options(input_option):
            print('You are now logged out')
            break

main()