from requests import get, post, delete

# корректные
print(get('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs',
           json={'team_leader': 'wgwgewgw',
                 'job': "ddbdadуиуукwega",
                 'work_size': 1352,
                 'collaborators': 'wrwwwrb',
                 'start_date': 2026,
                 'end_date': 2027,
                 'is_finished': False}).json())
print(delete('http://localhost:5000/api/v2/jobs/4').json())
# не корректные
print(post('http://localhost:5000/api/v2/jobs', json={'job': 'wgwgewgw'}).json())
print(delete('http://localhost:5000/api/v2/jobs/цутцштцйушпйошпош'))
