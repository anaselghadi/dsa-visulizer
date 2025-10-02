from enum import Enum
class cellstate(Enum):
    path = 0
    wall = 1
    start = 2
    end = 3
class Maze :
    def __init__(self, width:int, length:int) -> None:
        self.width = width 
        self.length = length
        self.grid = [[cellstate.path for _ in range(length)] for _ in range(width)]
        self.start_pos = (0, 0) 
        self.end_pos = (width - 1, length - 1)
        self.grid[0][0] = cellstate.start
        self.grid[width-1][length-1] = cellstate.end
    def get_cell_state(self, row:int,col:int):
        return self.grid[row][col]
    def set_cell_state(self, row:int,col:int,state:cellstate):
        self.grid[row][col] = state

if __name__ == "__main__":
    maze = Maze(5,5)   
    # for i, row in enumerate(maze.grid):
       
    #     for cell in row:
    #         print(f"{cell.value} ", end="")
    #     print()