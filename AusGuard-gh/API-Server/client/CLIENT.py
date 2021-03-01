import requests


json = {
    'Password': 'Summer2021',
    'Email': 'email@example.com'
}

headers = {
    'Username': 'Username1234',
    'Server': 'example.com',
    'Email': 'email@example.com',
    'Password': 'Summer2021'
}

res = requests.post('http://localhost/new/', headers=headers, json=json)
print(res.content)


# These are the valid addresses, just make sure that headers and
# JSON are connect to assure correct usage.
"""
http://localhost/new/
http://localhost/get/
http://localhost/edit/
"""