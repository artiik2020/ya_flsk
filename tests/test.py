from requests import get, post, delete

# корректные
print(get('http://localhost:5000/api/v2/users').json())
print(post('http://localhost:5000/api/v2/users',
           json={'surname': 'wgwgewgw',
                 'name': "ddbdadуиуукwega",
                 'age': 1352,
                 'position': 'wrwwwrb',
                 'speciality': 'egqggqeg',
                 'address': 'qegqegqeqeg',
                 'email': 'qegqegqegqewgq'}).json())
print(delete('http://localhost:5000/api/v2/users/4').json())
# не корректные
print(post('http://localhost:5000/api/v2/users', json={'surname': 'wgwgewgw'}).json())
print(delete('http://localhost:5000/api/v2/users/цутцштцйушпйошпош'))
