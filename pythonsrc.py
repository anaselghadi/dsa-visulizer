from enum import Enum
import random
from flask import Flask, jsonify, render_template 
class CellState(Enum):
    PATH = 0
    WALL = 1
    START = 2
    END = 3
class Maze :
    def __init__(self, width:int, length:int) -> None:
        self.width = width 
        self.length = length
        self._grid = [[CellState.PATH for _ in range(length)] for _ in range(width)]
        self.start_pos = (0, 0) 
        self.end_pos = (width - 1, length - 1)
        self._grid[0][0] = CellState.START
        self._grid[width-1][length-1] = CellState.END


    def generate_random_walls(self, wall_probability:float) -> None:
        if not (0 <= wall_probability <= 1):
            raise ValueError("Wall probability must be between 0 and 1")
        for i in range(self.width):
            for j in range(self.length):
                if (i, j) != self.start_pos and (i, j) != self.end_pos:
                    if random.random() < wall_probability:
                        self.set_cell_state(i, j, CellState.WALL)
                    else:
                        self.set_cell_state(i, j, CellState.PATH)
    def get_cell_state(self, row:int,col:int):
        if(row<0 or row>=self.width or col<0 or col>=self.length):
            raise IndexError("Cell position out of bounds")
        return self._grid[row][col]

    
    def set_cell_state(self, row:int,col:int,state:CellState)-> None:
        if(row<0 or row>=self.width or col<0 or col>=self.length) :
            raise IndexError("Cell position out of bounds")
        if(self._grid[row][col]==CellState.START or self._grid[row][col]==CellState.END):
            raise ValueError("Cannot change the state of start or end cell")    
        

        self._grid[row][col] = state
            
    def move_terminal(self, new_row:int,new_col:int,terminal:CellState)-> None:
        if(terminal!=CellState.START and terminal!=CellState.END):
            raise ValueError("Terminal must be either start or end")
        if(new_row<0 or new_row>=self.width or new_col<0 or new_col>=self.length):
            raise IndexError("New position out of bounds")
        if(terminal==CellState.START):
            old_row, old_col = self.start_pos
            self.start_pos = (new_row,new_col)
        else:
            old_row, old_col = self.end_pos
            self.end_pos = (new_row,new_col)
        if(self._grid[new_row][new_col]==CellState.WALL):
            raise ValueError("Cannot move terminal to a wall cell")
        self._grid[old_row][old_col] = CellState.PATH
        self._grid[new_row][new_col] = terminal
        
    @property
    def grid(self):
        return self._grid
    

    def __str__(self):
        maze_str = ""
        symbol_map = {
            CellState.PATH: " ",
            CellState.WALL: "#",
            CellState.START: "S",
            CellState.END: "E"
        }
        for row  in self.grid:
            maze_str += "".join([symbol_map[cell] for cell in row]) + "\n"

        return maze_str
    
    
#*** FLASK APPLICATION INITIALIZATION***
app = Flask(__name__)
Maze_instance = Maze(15, 15)
Maze_instance.generate_random_walls(0.3)

# ***FLASK ROUTES (The API and Frontend Pages)***
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/api/get_maze')
def get_maze_data():
    grid_values = [
        [cell.value for cell in row] 
        for row in Maze_instance.grid
    ]
    
    # Return a JSON object
    return jsonify({
        'grid': grid_values,
        'width': Maze_instance.width,
        'length': Maze_instance.length,
        'start': Maze_instance.start_pos,
        'end': Maze_instance.end_pos
    })

if __name__ == "__main__":
    app.run(debug=True)

  