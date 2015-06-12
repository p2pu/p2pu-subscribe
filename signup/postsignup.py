import requests
import json
import re
import sys

def signup(email, questions):

    #TODO get CSRF token
    csrf_url = 'http://localhost:8000'
    resp = requests.get(csrf_url)
    match = re.search(u".*csrfmiddlewaretoken'\ value='(?P<token>[a-z,A-Z,0-9]+)'", resp.text)
    csrf_token = match.groups('token')[0]

    signup_url = 'http://localhost:8000/signup'
    signup_data = {
        'csrfmiddlewaretoken': csrf_token,
        'email': email,
    }
    signup_data.update(questions)

    resp = requests.post(signup_url, data=signup_data, cookies=resp.cookies)
    if resp.status_code != 200:
        print(resp.text)

signup(**json.loads(sys.argv[1]))
