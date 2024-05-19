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