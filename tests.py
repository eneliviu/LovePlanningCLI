l = [['user_id', 'user_name', 'email', 'password'], ['1', 'jodo', 'jodo@email.com', 'Password12'], ['2', 'jado', 'jado@email.com', 'Password12']] 
d_keys =  l[0]
d = {d_keys[i]:[s[i] for s in l[1:]] for i in range(len(d.keys())) }
print(d)
'Password12' in d['password']


# def list_tasks(user_id:str) -> list:
#     tasks = SHEET.worksheet(TASKS)
#     task_data = tasks.get_all_values()
#     user_task = make_dict_from_nested_lists(task_data)

#     idx_task = [i for i in range(len(user_task['user_id'])) if user_task['user_id'][i] == user_id]
#     user_task = [t[1:] for t in [task_data[1:][i] for i in idx_task]]
    
#     print('Your tasks are listed below:')
#     print(tabulate(user_task, headers = task_data[0][1:]))

#     # Output Formatting: https://www.geeksforgeeks.org/python-output-formatting/
#     # d_keys = list(user_task.keys())[2:]
#     # for key in d_keys:
#     #     print(key, ":", [user_task[key][i] for i in idx_task])
    
#     return user_task


task_remove_idx = input('Please enter the indexes of the tasks to be removed.'
                            'Use commas to separate multiple entries: \n')
    
    #validate_task_id()

    print(f'you selected: {task_remove_idx}')
    task_remove_idx = int(task_remove_idx) + 1 


def validate_password_length(user_password:str) -> bool:
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


def validate_user_password_capital(user_password:str) -> bool:
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


def validate_user_password_numerals(user_password:str) -> bool:
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



# @dataclass
# class Defaults:
#     USERS: str = 'users'
#     TASKS: str = 'tasks'
#     #STATIC_OPTIONS: list['str'] = field(['y', 'n'])
#     USER_HEADER:list = field(default=['user_id','user_name','email','password'])
    