from flask import Flask, request
import dill

app = Flask(__name__)


@app.route('/registerFunction', methods=['POST'])
def registerPlayer():
    payload = request.data
    player = None
    try:
        f = dill.loads(payload)
        player = request.headers.get("Player")
        print(player, ' function received')
        with open(player + ".blob", 'wb') as outfile:
            dill.dump(f, outfile)
    except Exception as e:
        print("player registration failed", e)
        return [str(e)]

    return str(["Registered Player: " + player + "successfully... :)"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
