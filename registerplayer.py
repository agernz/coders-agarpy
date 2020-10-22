import requests
import dill as pickle
from updatePlayer import update_player


def register_player(name, func):
    url = "http://pabloeckardt.com:3000/registerFunction"
    payload = "data"
    headers = {
        'player': name,
        'Content-Type': 'text/plain'
    }
    payload = pickle.dumps(func)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text.encode('utf8'))

########  Type the name of your blob here ###########
PLAYER_NAME = "bob"
####################################################

register_player(PLAYER_NAME, update_player)
