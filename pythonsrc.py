from enum import Enum
class CellState(Enum):
    path = 0
    wall = 1
    start = 2
    end = 3
class Maze :
    def __init__(self, width:int, length:int) -> None:
        self.width = width 
        self.length = length
        self.grid = [[CellState.path for _ in range(length)] for _ in range(width)]
        self.start_pos = (0, 0) 
        self.end_pos = (width - 1, length - 1)
        self.grid[0][0] = CellState.start
        self.grid[width-1][length-1] = CellState.end
    def get_grid(self):
        return self.grid
    
    
    def get_cell_state(self, row:int,col:int):
        if(row<0 or row>=self.width or col<0 or col>=self.length):
            raise IndexError("Cell position out of bounds")
        return self.grid[row][col]
    
    
    def set_cell_state(self, row:int,col:int,state:CellState)-> None:
        
        if(row<0 or row>=self.width or col<0 or col>=self.length) :
            raise IndexError("Cell position out of bounds")
        if(self.grid[row][col]!=CellState.start and self.grid[row][col]!=CellState.end):
            self.grid[row][col] = state
        elif state==CellState.start or state==CellState.end:
            self.grid[row][col] = state
            if state==CellState.start:
                self.start_pos = (row,col)
            else:
                self.end_pos = (row,col)
            
        
    def __str__(self):
        maze_str = ""
        for row  in self.grid:
            maze_str += " ".join([str(cell.value) for cell in row]) + "\n"
        return maze_str

if __name__ == "__main__":
    maze = Maze(5,5)   
    print(maze)
    # for i, row in enumerate(maze.grid):
       
    #     for cell in row:
    #         print(f"{cell.value} ", end="")
    #     print()