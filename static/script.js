const CELL_STATE_MAP = {
    0: 'path',
    1: 'wall',
    2: 'start',
    3: 'end'
};

const mazeContainer = document.getElementById('maze-container');
const statusText = document.getElementById('maze-status');

// Function to fetch and render the maze
async function loadMaze() {
    statusText.innerText = "Loading...";
    try {
        const response = await fetch('/api/get_maze');
        const data = await response.json();
        
        // Update CSS variables for grid dimensions
        document.documentElement.style.setProperty('--maze-cols', data.length);
        document.documentElement.style.setProperty('--maze-rows', data.width);

        renderGrid(data);
        statusText.innerText = "Ready";
    } catch (err) {
        statusText.innerText = "Error loading maze";
        console.error(err);
    }
}

function renderGrid(data) {
    mazeContainer.innerHTML = '';
    const { grid, width, length } = data;

    for (let r = 0; r < width; r++) {
        for (let c = 0; c < length; c++) {
            const cell = document.createElement('div');
            const state = grid[r][c];
            cell.className = `cell ${CELL_STATE_MAP[state]}`;
            cell.id = `cell-${r}-${c}`;
            mazeContainer.appendChild(cell);
        }
    }
}

// Function to handle the "New Maze" button without refreshing the page
async function handleRegenerate() {
    statusText.innerText = "Generating...";
    try {
        // We tell the server to shuffle the walls
        await fetch('/api/regenerate', { method: 'POST' });
        
        // Clear any remaining solution classes before re-loading
        const cells = document.querySelectorAll('.solution');
        cells.forEach(cell => cell.classList.remove('solution'));
        
        // After server is done, we simply reload the maze data
        await loadMaze();
    } catch (err) {
        statusText.innerText = "Error regenerating";
        console.error(err);
    }
}

// Function to fetch the solution and animate it
async function solveMaze() {
    statusText.innerText = "Solving...";
    try {
        const response = await fetch('/api/solve');
        const data = await response.json();
        const path = data.path;

        if (path.length === 0) {
            statusText.innerText = "No Path Found!";
            return;
        }

        path.forEach((coords, index) => {
            setTimeout(() => {
                const [r, c] = coords;
                const cell = document.getElementById(`cell-${r}-${c}`);
                if (!cell.classList.contains('start') && !cell.classList.contains('end')) {
                    cell.classList.add('solution');
                }
                if (index === path.length - 1) statusText.innerText = "Solved!";
            }, index * 20);
        });
    } catch (err) {
        statusText.innerText = "Solver Error";
        console.error(err);
    }
}

// Updated Event Listeners
document.getElementById('regenerate-btn').addEventListener('click', handleRegenerate);
document.getElementById('solve-btn').addEventListener('click', solveMaze);

// Initial Load
window.addEventListener('DOMContentLoaded', loadMaze);