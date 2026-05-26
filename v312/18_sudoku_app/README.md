# 🧩 Sudoku Creator & Solver

A complete Sudoku application built with **Python** and **Flask**. This project combines a puzzle generator, a backtracking solver with step-by-step animation, and a web interface for playing and solving puzzles.

## 🚀 Features

- **Puzzle Generation**: Create valid Sudoku puzzles with three difficulty levels (Easy, Medium, Hard).
- **Deterministic Puzzles**: Support for a random seed to recreate the same puzzle.
- **Animated Solver**: A backtracking solver that records every attempt, allowing users to watch the solving process step-by-step.
- **Subprocess Execution**: The solver is implemented as a standalone script and can be called via a subprocess for performance comparison.
- **Interactive UI**:
  - Numpad and keyboard input.
  - Real-time board validation (detects conflicts).
  - Play/Pause/Step controls for the solver animation.
  - Variable animation speed.
- **Board Management**: Options to reset to the original puzzle or clear the board.

---

## 📁 Project Structure

```text
18_sudoku_app/
├── sudoku_app.py         # Flask startup and server configuration
├── sudoku_engine.py      # Core logic: Generator, Validator, and Solver
├── sudoku_solver.py      # Standalone solver script for subprocess calls
├── sudoku_helpers.py     # Flask routes and API logic
└── sudoku_templates/      # UI templates
    ├── base.html         # Shared layout and styling
    └── index.html        # Game board and control panel
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Install Flask:
```bash
pip install flask
```

### 2. Core Logic: The Engine (`sudoku_engine.py`)

The engine handles the mathematical logic of Sudoku.

#### A. Validation Logic
Implement `is_valid(board, row, col, num)`:
- Check the **row** to see if the number already exists.
- Check the **column** to see if the number already exists.
- Check the **3x3 box** by calculating the box start indices `(row // 3) * 3` and `(col // 3) * 3`.

#### B. Backtracking Solver
Implement the `solve(board)` function:
1. Find the first empty cell (value 0). If none exist, the board is solved.
2. Iterate through numbers 1–9.
3. If a number is valid in that cell, place it and recursively call `solve()`.
4. If the recursive call returns False, reset the cell to 0 (backtrack) and try the next number.

#### C. Step-Recording Solver
Implement `solve_with_steps(board)`:
- Similar to the backtracking solver, but instead of just returning a boolean, append an object to a `steps` list every time a number is placed or removed.
- Each step should contain: `row`, `col`, `num`, and `action` ('place' or 'backtrack').

#### D. Puzzle Generator
Implement `generate(difficulty, seed)`:
1. Start with an empty board and fill it completely using the `solve()` function (shuffled numbers ensure randomness).
2. Determine how many "clues" to keep based on difficulty (e.g., Easy=36, Medium=27, Hard=22).
3. Randomly remove cells one by one.
4. **Crucial**: After removing a cell, verify that the puzzle still has a unique solution. If not, restore the cell and try another.

---

### 3. Standalone Solver (`sudoku_solver.py`)

Create a separate script that:
- Takes an 81-character puzzle string as a command-line argument.
- Converts the string into a 9x9 board.
- Solves the board and measures the time taken (`time.perf_counter_ns()`).
- Prints the result as a JSON string: `{"solution": "...", "elapsed_ns": ..., "solved": ...}`.

---

### 4. Flask API Integration (`sudoku_helpers.py`)

Define the endpoints to connect the frontend to the engine:

- **`/generate` (POST)**: Calls `engine.generate()`, converts the board to a flat list, and returns the puzzle and solution as JSON.
- **`/solve` (POST)**: 
  - Runs the step-recording solver to provide data for the animation.
  - Optionally calls `sudoku_solver.py` via `subprocess.run()` to compare the performance of the standalone script versus the in-process solver.
- **`/validate` (POST)**: Takes the current board state and iterates through all non-empty cells to check for conflicts using `engine.is_valid()`.

---

### 5. Application Entry (`sudoku_app.py`)
- Initialize Flask.
- Register routes using `sudoku_helpers.setup_routes(app)`.
- Run the app on port 8117.

### 6. Frontend Development (`sudoku_templates/`)
- **`base.html`**: Set up a dark-themed layout with a responsive grid.
- **`index.html`**:
  - **The Board**: A 9x9 grid of inputs. Style it so that 3x3 blocks are visually distinct (e.g., thicker borders).
  - **Numpad**: Buttons for numbers 1–9 to allow easy input.
  - **Controls**: Buttons for Generate, Solve, Validate, and Clear.
  - **Animation Logic**: JavaScript that reads the `steps` array from the `/solve` response and updates the board cells one by one at a specified interval.

---

## 🏃 How to Run

1. Run the server:
   ```bash
   python sudoku_app.py
   ```
2. Open your browser and navigate to:
   **http://localhost:8117**

---

## 📚 Key Concepts Demonstrated

- **Backtracking Algorithm**: A depth-first search approach to solving constraint satisfaction problems.
- **Recursive Problem Solving**: Using recursion to explore all possible number combinations.
- **Puzzle Generation Logic**: The process of creating a solvable puzzle with a unique solution.
- **Subprocess Management**: Using Python's `subprocess` module to execute and communicate with external scripts.
- **Real-time Web Animation**: Using JavaScript to playback a recorded sequence of algorithmic steps.
- **Complexity Analysis**: Measuring execution time in nanoseconds for algorithm comparison.
