from flask import Flask, request
import dill
from player import Player

app = Flask(__name__)


@app.route('/registerFunction', methods=['POST'])
def registerPlayer():
    payload = request.data
    player = None
    try:
        player = request.headers.get("Player")
        f = dill.loads(payload)
        file_name = "./player-blobs/"+player + ".blob"
        with open(file_name, 'wb') as outfile:
            dill.dump(f, outfile)
    except Exception as e:
        error = "player registration failed. Error: " + str(e)
        print(error)
        return str(error)

    return str(["Registered Player: " + player + " successfully... :)"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
