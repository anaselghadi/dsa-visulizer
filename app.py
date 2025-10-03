from flask import Flask
from pythonsrc import Maze
from enum import Enum
import random
app = Flask(__name__)
Maze_instance = Maze(10, 10)
Maze_instance.generate_random_walls(0.3)
@app.route("/")
def index():
    return str(Maze_instance)
if __name__ == "__main__":
    app.run(debug=True)
