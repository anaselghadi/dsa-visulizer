const CELL_STATE_MAP = {
    0: 'path',
    1: 'wall',
    2: 'start',
    3: 'end'
};

const mazeContainer = document.getElementById('maze-container');
const statusText = document.getElementById('maze-status');

/**
 * Fetches the current maze state from the server and renders the grid.
 */
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

/**
 * Creates the div elements representing each cell in the maze.
 */
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

/**
 * Triggers a maze regeneration on the server and reloads the UI.
 */
async function handleRegenerate() {
    statusText.innerText = "Generating...";
    try {
        // Clear existing visuals immediately for responsiveness
        const cells = document.querySelectorAll('.visited, .solution');
        cells.forEach(cell => {
            cell.classList.remove('visited', 'solution');
        });

        await fetch('/api/regenerate', { method: 'POST' });
        await loadMaze();
    } catch (err) {
        statusText.innerText = "Error regenerating";
        console.error(err);
    }
}

/**
 * Fetches the solution and animates both exploration (yellow) and path (cyan).
 */
async function solveMaze() {
    statusText.innerText = "Exploring...";
    try {
        const response = await fetch('/api/solve');
        const data = await response.json();
        const { path, visited } = data;

        // Clear previous solve attempts
        const oldSolve = document.querySelectorAll('.visited, .solution');
        oldSolve.forEach(c => c.classList.remove('visited', 'solution'));

        // 1. Animate Exploration (Visited Cells in Yellow)
        for (let i = 0; i < visited.length; i++) {
            const [r, c] = visited[i];
            const cell = document.getElementById(`cell-${r}-${c}`);
            
            if (cell && !cell.classList.contains('start') && !cell.classList.contains('end')) {
                cell.classList.add('visited');
                // Short delay to see the BFS expansion effect
                await new Promise(resolve => setTimeout(resolve, 5));
            }
        }

        if (!path || path.length === 0) {
            statusText.innerText = "No Path Found!";
            return;
        }

        // 2. Animate Final Path (Solution in Cyan)
        statusText.innerText = "Path Found!";
        for (let i = 0; i < path.length; i++) {
            const [r, c] = path[i];
            const cell = document.getElementById(`cell-${r}-${c}`);
            
            if (cell && !cell.classList.contains('start') && !cell.classList.contains('end')) {
                cell.classList.remove('visited');
                cell.classList.add('solution');
                // Slower delay to make the final path stand out
                await new Promise(resolve => setTimeout(resolve, 25));
            }
        }
        statusText.innerText = "Solved!";
    } catch (err) {
        statusText.innerText = "Solver Error";
        console.error(err);
    }
}

// Event Listeners
document.getElementById('regenerate-btn').addEventListener('click', handleRegenerate);
document.getElementById('solve-btn').addEventListener('click', solveMaze);

// Initial Load
window.addEventListener('DOMContentLoaded', loadMaze);