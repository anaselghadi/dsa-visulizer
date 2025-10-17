// static/script.js

// 1. Mapping from Python Enum value (int) to CSS Class name (string)
const CELL_STATE_MAP = {
    0: 'path', 
    1: 'wall', 
    2: 'start', 
    3: 'end',   
};

async function drawMaze() {
    const container = document.getElementById('maze-container');
    container.innerHTML = 'Fetching maze data...'; // Reset loading message

    try {
        const response = await fetch('/api/get_maze');
        const data = await response.json();

        // Destructure essential properties
        const { grid, width, length, start, end } = data;

        // 3. Set CSS Grid dimensions dynamically
        document.documentElement.style.setProperty('--maze-cols', length);
        // Note: For a square grid, setting rows isn't strictly necessary if cols determines the width, 
        // but setting both is safer for future adjustments:
        document.documentElement.style.setProperty('--maze-rows', width); 

        // Clear the container
        container.innerHTML = ''; 

        // 4. Loop and Create Elements
        for (let r = 0; r < width; r++) {
            for (let c = 0; c < length; c++) {
                const cellValue = grid[r][c];
                const cellDiv = document.createElement('div');
                
                // Add the base class and the state-specific color class
                cellDiv.className = `cell ${CELL_STATE_MAP[cellValue]}`;

                // Add content for Start/End
                if (r === start[0] && c === start[1]) {
                    cellDiv.textContent = 'S';
                } else if (r === end[0] && c === end[1]) {
                    cellDiv.textContent = 'E';
                }
                
                container.appendChild(cellDiv);
            }
        }

    } catch (error) {
        console.error("Error fetching or drawing maze:", error);
        container.innerHTML = 'Failed to load maze. Check server connection.';
    }
}

// 5. Initial Call
window.onload = drawMaze;