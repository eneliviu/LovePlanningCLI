l = [['user_id', 'user_name', 'email', 'password'], ['1', 'jodo', 'jodo@email.com', 'Password12'], ['2', 'jado', 'jado@email.com', 'Password12']] 
d_keys =  l[0]
d = {d_keys[i]:[s[i] for s in l[1:]] for i in range(len(d.keys())) }
print(d)
'Password12' in d['password']