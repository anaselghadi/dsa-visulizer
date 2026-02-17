🧩 Interactive Maze Solver (BFS)A full-stack web application that generates random mazes and finds the shortest path using the Breadth-First Search (BFS) algorithm.🛠️ Installation GuideFollow these steps in your terminal to set up the project environment:1. PrerequisitesEnsure you have Python installed. You can check by running:python --version  
2\. Setup Virtual Environment (Recommended)This keeps your project dependencies isolated. Create the environment  
python -m venv venv

Activate it (Windows)
=====================

venv\\Scripts\\activate

Activate it (macOS/Linux)
=========================

source venv/bin/activate  
3\. Install FlaskThe only external library required for this project:pip install flask  
🎮 How to Run and Use1. Start the BackendExecute the Python script to launch the local web server:python app.py  
Note: The terminal will display Running on [http://127.0.0.1:5000](http://127.0.0.1:5000). Keep this window open while using the app.2. Open the UILaunch your web browser and navigate to:[http://127.0.0.1:50003](http://127.0.0.1:50003). Controls\[New Maze\] Button: Sends a POST request to /api/regenerate to shuffle the grid layout.\[Solve Path\] Button: Triggers the BFS algorithm. Watch the Yellow exploration phase followed by the Cyan shortest path.📂 Project StructureOrganize your files exactly like this for the Flask server to function:/maze-solver  
├── app.py <-- Main Python Logic (Maze class & API)  
├── README.md <-- Documentation  
├── static/ <-- Frontend Assets  
│ ├── style.css <-- Grid styling & Animations  
│ └── script.js <-- API communication & Logic  
└── templates/ <-- HTML Files  
└── index.html <-- Main Dashboard  
🎨 Visual LegendElementColorDescriptionStart🟩 GreenThe starting point of the search.End🟥 RedThe target destination.Walls⬛ Dark GrayObstacles that cannot be passed.Exploration🟨 YellowAnimated BFS search (visited nodes).Path🟦 CyanThe final shortest route found.Developer: anaselghadiDeveloped as a learning project for Python Flask and Algorithm Visualization.
