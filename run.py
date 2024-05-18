# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
import regex as re
from tabulate import tabulate
import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('LovePlanning')


# New users
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
    dictionary comprehension.
    The keys are the values in the first list (list_data[0]) of the list_data entry.
    Each dictionary key receives a list of values from the remaining lists of list_data argument.        
    '''
    d_keys = list_data[0]
    return {d_keys[i]:[s[i] for s in list_data[1:]] for i in range(len(d_keys)) }  


# For Registered Users:


def validate_log_input(user_input:str) -> bool:
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
    The name string must not be empty and must cotain two strings separated by comma,
    It works for registered users, as well as for new users trying to register.
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

def match_user_passwords(user_data:dict, user_name:str, user_password:str) -> bool:
    '''
    Validates existing passwords by matching them against the
    records in the 'password'- column of the 'users'- sheet.  
    '''
    users = SHEET.worksheet('users')
    user_data = users.get_all_values()
    d_keys = user_data[0]
    user_data = {d_keys[i]:[s[i] for s in user_data[1:]] for i in range(len(d_keys)) }
    password = user_data['password'][user_data['user_name'] == user_name]
    
    if user_password == password:
        return True
    else:
        print('Passwords do not match, please try again')
        return False

def user_login() -> list:
    '''
    Validates credentials (username and password) from user input.
    The while-loop runs until the user enters the correct data. 
    Returns the user data from the 'tasks'- google sheet as a dictionary with 
    the keys corresponig to the column names and the values as the column data.
    '''
    while True:

        user_input = input('Please enter your username and password separated by comma :')

        # Validate user_input: two strings separated by comma:
        if validate_username(user_name):

            # Retrieve the input components: username [0] and password [1]
            user_input = user_input.split(',')
            user_name = user_input[0].strip()
            user_password = user_input[1].strip()

            # Get the user data from the 'users' Google worksheet:
            users = SHEET.worksheet('users')
            user_data = users.get_all_values()

            # Create a dictionary from the user data (list of lists):
            # keys: column names (worksheet header)
            # values: column data (without the header).
            user_data = make_dict_from_nested_lists(user_data)

            # Check if username and password exist:
            # Username first, as there is no need to retrieve passords 
            # for non-existing usernames. 
        
            # If everything True, break the while loop:
            if match_user_name(user_data,
                                user_name) & \
                match_user_passwords(user_data,
                                    user_name,
                                    user_password):
                
            
                break
    
    # Everything seems to be fine, return the user id:
    user_id = user_data['user_id'][user_data['user_name'].index(user_name)]
    return(user_id)
    

def user_help():
    print('This is the functionality')


def list_tasks(user_id:str):
    tasks = SHEET.worksheet('tasks')
    task_data = tasks.get_all_values()
    user_task = make_dict_from_nested_lists(task_data)

    idx_task = [i for i in range(len(user_task['user_id'])) if user_task['user_id'][i] == user_id]
    user_task = [t[1:] for t in [task_data[1:][i] for i in idx_task]]
    
    print('\n Your tasks are listed below:')
    print(tabulate(user_task, headers = task_data[0][1:]))

    # Output Formatting: https://www.geeksforgeeks.org/python-output-formatting/
    # d_keys = list(user_task.keys())[2:]
    # for key in d_keys:
    #     print(key, ":", [user_task[key][i] for i in idx_task])
    

def main_menu_options():
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

def handle_input_options(input_option:int):
    '''
    Takes the menu selection from user input and handles the menu item logic.  
    '''
    while True:
        if input_option == 1:
            user_cred = user_login() # validates and returns credentials for regsistered users
            task_handler(user_cred)  # takes user_id and returns the user tasks

            break
        elif input_option == 2:
            user_register()
            break
        elif input_option == 3:
            user_help()
        else:
            break


def task_handler(user_data) -> None:
    '''
    Lists task handling options for registered users.
    Each option  
    '''
    print('\nLogin successful! Please enter an option:')
    print('1 (view active tasks), 2 (add task), 3 (delete task), 4 (exit)')

    while True:
        user_choice = int(input())
        if(user_choice not in [1,2,3,4]):
            print('Please enter a valid option:')
            print('1 (view active tasks), 2 (add task), 3 (delete task), 4 (exit)')
        else:
            if user_choice == 1:
                list_tasks(user_data)
                break
            elif user_choice == 2:
                user_register()
            elif user_choice == 3:
                user_help()
            else:
                print('You are logged out')
                break



def main():
    print('Welcome to LovePlanning, the Ultimate Task Management Tool!')
    input_option = main_menu_options()
    handle_input_options(input_option)



main()