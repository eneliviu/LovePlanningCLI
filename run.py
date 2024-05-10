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

#users = SHEET.worksheet('users')
#user_data = users.get_all_values()
#print(user_data)

def validate_user_name(user_data:str):
    '''
    The name string must not be empty ot contain
    alphanumeric and/or underscores. 
    '''
    
    try: 
        if not user_data.isalnum() or '_' not in user_data:
            raise NameError('Names should not contain underscores or numerals')
    except NameError as e:
        print(f'Invalid data: {e}, pleae try again.\n')
        return False
    
    print(f'You entered: {user_data}')
    return True

def validate_password_length(user_data:str):
    '''
    Check if the string has minimum 8 characters:
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
    Check if the password contains at least one capital letter. 
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
    Check if the password contains at least two numerals.
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
    

def user_login():
    user_name = input('Please enter your user name: ')
    validate_user_name(user_name)
    user_password = input('Please enter your pasword: ')
    validate_password_length(user_password)
    validate_user_password_capital(user_password)
    validate_user_password_numerals(user_password)
    
def user_register():
    user_name = input('Please enter your user name: ')
    validate_user_name(user_name)
    user_password = input('Please enter your pasword: ')
    validate_user_name(user_password)
    user_email = input('Please enter your pasword: ')
    validate_user_name(user_email)

def exit_app():
    print('Exit')

def get_user_data():
    '''
    Gets input data to register a new user. Run a while loop to collect
    a valid string of data from the user via the terminal. 
    The loop will repeatedly request data, until it is valid. 
    '''
   
    print('Please enter an option:')
    print('Press 1 to Log in:')
    print('Press 2 to Register:')
    print('Press 3 to Exit:')

    while True:
        user_data = int(input())
        if(user_data not in [1,2,3]):
            print('Please enter a valid option: 1 (Log in), 2 (Register) or 3 (Exit) application')
        else:
            if user_data == 1:
                user_login()
            elif user_data == 2:
                user_register()
            else:
                exit_app() 
            break
    return user_data


def main():
    print('Welcome to LovePlanning, the ultimate task Management tool! :\n')
    user_creds = get_user_data()

main()