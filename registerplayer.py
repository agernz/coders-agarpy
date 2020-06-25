import dill as pickle
import requests
import sys
from player import Player
import inspect

def getDecisionFunction(module):
    return list(filter(lambda x: x[0] is "make_decision", inspect.getmembers(module)))[0]

def registerPlayer(name, f):
    url = "http://pabloeckardt.com:3000/registerFunction"
    payload = "data"
    headers = {
        'player': name,
        'Content-Type': 'text/plain'
    }
    payload = pickle.dumps(f)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))

########  Type the name of your blob here ###########
player_name = "bob"
####################################################

function = getDecisionFunction(Player)[1]
registerPlayer(player_name, function)
