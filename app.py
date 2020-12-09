from world import World
from flask import Flask, render_template

app = Flask(__name__)

world = World()

@app.route('/')
def load_game():
    return render_template('index.html')

@app.route('/updateGame')
def update_game():
    return world.update()
