# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

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
    Gets input data to register a new user. Run a while loop to collect
    a valid string of data from the user via the terminal. 
    The loop will repeatedly request data, until it is valid. 
    '''
   
    print(f'You entered: {user_data}')

def validate_user_password(user_data:str):
     print(f'You entered: {user_data}')

def validate_user_email(user_data:str):
     print(f'You entered: {user_data}')


def user_login():
    user_name = input('Please enter your user name: ')
    validate_user_name(user_name.lower())
    user_password = input('Please enter your pasword: ')
    validate_user_name(user_password.lower())
    
def user_register():
    user_name = input('Please enter your user name: ')
    validate_user_name(user_name.lower())
    user_password = input('Please enter your pasword: ')
    validate_user_name(user_password.lower())
    user_email = input('Please enter your pasword: ')
    validate_user_name(user_email.lower())

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