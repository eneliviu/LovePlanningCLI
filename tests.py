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
            users = SHEET.worksheet(USERS)
            user_data = users.get_all_values()
            
            # Retrieve user information (row) from the 'users' worksheet:
            # users.row_values( users.col_values(2).index('jodo')+1) 

            # Create a dictionary from the user data (list of lists):
            # keys: column names (worksheet header)
            # values: column data (without the header).
            #user_data = make_dict_from_nested_lists(user_data)

            user_data = get_user_info(USERS, user_name, 'user_name')

            # Check if username and password exist:
            # Username first, as there is no need to retrieve passords 
            # for non-existing usernames. 
        
            # If username and password OK, break the while loop:
            # if match_user_name(user_data,
            #                     user_name) & \
            #     match_user_passwords(user_data,
            #                         user_name,
            #                         user_password):
            #     break

            if match_user_credentials(user_data, user_name, user_password):
                break
    
    # Everything seems to be fine, return the user id:
    user_id = user_data['user_id'][user_data['user_name'].index(user_name)]
    #user_tasks = list_tasks_simple(user_id)

    return user_id