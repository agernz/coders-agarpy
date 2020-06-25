import dill as pickle
import requests
import sys

def registerPlayer(f):
    url = "http://pabloeckardt.com:3000/registerFunction"
    payload = "data"
    headers = {
        'player': 'pablo',
        'Content-Type': 'text/plain'
    }
    payload = pickle.dumps(f)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))
