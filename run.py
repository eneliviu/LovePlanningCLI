# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
import regex as re

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


# Registered users:

def validate_username(user_name:str):
    '''
    The name string must not be empty ot contain
    alphanumeric and/or underscores. It works for registered users, 
    as well as for new users trying to register.
    '''
    try: 
        if len(user_name) < 2:
            raise NameError('Username should not contain at least three characters')
    except NameError as e:
        print(f'Invalid username: {e}, please try again.\n')
        return False
    
    return True

def match_user_name(user_data:dict, user_name:str):
    '''
    Validates existing usernames by matching them against the
    records in the 'username'- column of the 'users'- sheet.  
    '''
    while True:
        if user_name in user_data['user_name']:
            print('Valid username')
            return True
        else:
            print('Username not found, please try again')
            return False


def fn():

    while True:

        user_input = input('Please enter your username and password separated by comma:')
        user_input = user_input.split(',')
        user_name = user_input[0].strip()
        user_password  = user_input[1].strip()

        if validate_username(user_name):
            print(user_name)
            users = SHEET.worksheet('users')
            user_data = users.get_all_values()
            d_keys = user_data[0]
            user_data = {d_keys[i]:[s[i] for s in user_data[1:]] for i in range(len(d_keys)) }

            if match_user_name(user_data,
                                user_name) & \
                match_user_passwords(user_data,
                                    user_name,
                                    user_password):
                print('Login successful!')
            
                break
    
    print(user_data)
    
    return user_data


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
        print('Valid password')
        return True
    else:
        print('Passwords do not match, please try again')
        return False

def user_login():

    user_input = input('Please enter your user name: ')
    username_ok = validate_username(user_name)

    
    user_password = input('Please enter your pasword: ')
    user_password_ok = match_user_passwords(user_name, user_password) 

    if username_ok & user_password_ok:
        print('Loggin succesfull')
        task_handler()



def user_help():
    print('This is the functionality')

def exit_app():
    print('Exit')

def task_handler():
    '''
    
    '''
    print('You are logged in, please enter an option:')
    print('1 to list the active tasks')
    print('2 to add new tasks')
    print('3 to delete tasks')
    print('4 to return to the main menu:')

    while True:
        user_choice = int(input())
        if(user_choice not in [1,2,3,4]):
            print('Please enter a valid option: 1 (View), 2 (Add), 3 (Delete), 4 (Return)')
        else:
            if user_choice == 1:
                print('User choce 1')
            elif user_choice == 2:
                user_register()
            elif user_choice == 3:
                user_help()
            else:
                exit_app() 
            break


def main_menu_options():
    '''
    Gets input data to register a new user. 
    Run a while loop to collect a valid string of data
    from the user via the terminal. The loop will repeatedly
    request user input data, until it is valid. 
    '''
    print('Please enter an option:')
    print('Press 1 to Log in:')
    print('Press 2 to Register:')
    print('Press 3 to Exit:')

    while True:
        input_option = int(input())
        if(input_option not in [1,2,3,4]):
            print('Please enter a valid option: 1 (Log in), 2 (Register), 3 (Help) or 4 (Exit) application')
        else:
            break
    return input_option


def handle_input_options(input_option:int):
    if input_option == 1:
        fn()
    elif input_option == 2:
        user_register()
    elif input_option == 3:
        user_help()
    else:
        exit_app()


def main():
    print('Welcome to LovePlanning, the ultimate task Management tool! :\n')
    input_option = main_menu_options()
    handle_input_options(input_option)



main()