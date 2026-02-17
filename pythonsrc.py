from flask import Flask, jsonify, render_template 
from enum import Enum
import random
from collections import deque

class CellState(Enum):
    PATH = 0
    WALL = 1
    START = 2
    END = 3

class Maze:
    def __init__(self, width:int, length:int) -> None:
        self.width = width 
        self.length = length
        self._grid = [[CellState.PATH for _ in range(length)] for _ in range(width)]
        self.start_pos = (0, 0) 
        self.end_pos = (width - 1, length - 1)
        self._grid[0][0] = CellState.START
        self._grid[width-1][length-1] = CellState.END

    def generate_random_walls(self, wall_probability:float) -> None:
        """Randomizes walls while keeping Start and End clear."""
        if not (0 <= wall_probability <= 1):
            raise ValueError("Wall probability must be between 0 and 1")
        for i in range(self.width):
            for j in range(self.length):
                if (i, j) != self.start_pos and (i, j) != self.end_pos:
                    if random.random() < wall_probability:
                        self.set_cell_state(i, j, CellState.WALL)
                    else:
                        self.set_cell_state(i, j, CellState.PATH)

    def get_cell_state(self, row:int, col:int):
        if(row < 0 or row >= self.width or col < 0 or col >= self.length):
            raise IndexError("Cell position out of bounds")
        return self._grid[row][col]

    def set_cell_state(self, row:int, col:int, state:CellState) -> None:
        if(row < 0 or row >= self.width or col < 0 or col >= self.length):
            raise IndexError("Cell position out of bounds")
        if(self._grid[row][col] == CellState.START or self._grid[row][col] == CellState.END):
            raise ValueError("Cannot change the state of start or end cell")    
        self._grid[row][col] = state
            
    def solve_bfs(self) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        """
        Finds the shortest path and the order of exploration.
        Returns: (path, visited_order)
        """
        start_row, start_col = self.start_pos
        queue = deque([(start_row, start_col)])
        
        # Track the order of exploration for the yellow animation
        visited_order = [] 
        visited_set = {self.start_pos}
        
        # Dictionary for path reconstruction: child -> parent
        parents = {self.start_pos: None} 
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            curr_row, curr_col = queue.popleft()
            visited_order.append((curr_row, curr_col))

            # Target reached
            if (curr_row, curr_col) == self.end_pos:
                path = []
                current = self.end_pos
                while current is not None:
                    path.append(current)
                    current = parents[current]
                return path[::-1], visited_order

            for dr, dc in directions:
                next_row, next_col = curr_row + dr, curr_col + dc
                next_pos = (next_row, next_col)

                if (0 <= next_row < self.width and 0 <= next_col < self.length and 
                    self._grid[next_row][next_col] != CellState.WALL and 
                    next_pos not in visited_set):
                    visited_set.add(next_pos)
                    parents[next_pos] = (curr_row, curr_col)
                    queue.append(next_pos)
        
        return [], visited_order

    @property
    def grid(self):
        return self._grid

# *** FLASK APPLICATION INITIALIZATION ***
app = Flask(__name__)

# Initialize a standard 20x20 maze
Maze_instance = Maze(20, 20)
Maze_instance.generate_random_walls(0.3)

@app.route("/")
def index():
    # Force a new maze layout on every full page refresh
    Maze_instance.generate_random_walls(0.3)
    return render_template('index.html')

@app.route('/api/get_maze')
def get_maze_data():
    """Returns the current grid state to the frontend."""
    grid_values = [[cell.value for cell in row] for row in Maze_instance.grid]
    return jsonify({
        'grid': grid_values,
        'width': Maze_instance.width,
        'length': Maze_instance.length,
        'start': Maze_instance.start_pos,
        'end': Maze_instance.end_pos
    })

@app.route('/api/regenerate', methods=['POST'])
def regenerate_maze():
    """Triggered by the 'New Maze' button for a smooth update."""
    Maze_instance.generate_random_walls(0.3)
    return jsonify({'status': 'success'})

@app.route('/api/solve')
def solve_maze():
    """Returns both the shortest path and the order of exploration."""
    path, visited = Maze_instance.solve_bfs()
    return jsonify({
        'path': path, 
        'visited': visited
    })

if __name__ == "__main__":
    app.run(debug=True)