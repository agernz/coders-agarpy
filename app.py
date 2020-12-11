from time import sleep
from world import World
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
# CHANGE URL
# socketio = SocketIO(app, cors_allowed_origins='https://glimmer-clean-paper.glitch.me')

world = World()

@app.route('/')
def load_game():
    return render_template('index.html')

@socketio.on('connected')
def on_connected(json):
    print('Connected to client: ' + str(json))
    while True:
        emit('update_game', world.update())
        sleep(.1)
        if not world.running:
            break

@socketio.on('restart')
def restart(json):
    print('restart')
    world.restart()

@socketio.on('disconnect')
def disconnected():
    print('Client disconnected')

if __name__ == "__main__":
    socketio.run(app)
