# 🐍 Snake Game with AI Mode

A classic Snake game implemented in Python using the `tkinter` library. This project demonstrates game state management, keyboard event handling, and the implementation of a basic AI using the Breadth-First Search (BFS) algorithm.

## 🚀 Features

- **Classic Gameplay**: Move the snake to eat food and grow longer.
- **Dynamic Scoring**: Earn 10 points for every piece of food eaten.
- **Game Over Conditions**: The game ends if the snake hits the boundaries of the grid or its own body.
- **Auto Mode (AI)**: A built-in AI that automatically finds the shortest path to the food using the BFS algorithm.
- **Control System**:
  - **Arrow Keys**: Change snake direction.
  - **'R' Key**: Restart the game after a Game Over.
  - **'Q' Key**: Quit the application.
  - **'A' Key**: Toggle between Manual and Auto mode.

---

## 📁 Project Structure

```text
17_snake_game/
├── snake_game.py    # Main game loop, state management, and rendering
└── snake_helpers.py # Keyboard handlers and AI (BFS) logic
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
This project uses `tkinter`, which is included in the Python standard library. No external packages are required.

### 2. Game State Management (`snake_game.py`)

#### Step 1: Define Constants and State
Create constants for directions (`UP=0, DOWN=1, LEFT=2, RIGHT=3`) and a `make_state` function that returns a dictionary containing:
- **Body Position**: Two lists (`body_x`, `body_y`) representing the segments, with index 0 as the head.
- **Movement**: Current direction and the corresponding coordinate deltas (`dx`, `dy`).
- **Game Status**: `score` and an `alive` boolean.
- **Food Position**: Randomly generated `food_x` and `food_y`.
- **Grid Size**: Dimensions of the game area.

#### Step 2: Core Game Logic
Implement the following functions:
- **`place_food(state)`**: Generate random coordinates for food. Ensure the food does not spawn on top of the snake's body by checking against the `body_x` and `body_y` lists.
- **`set_direction(state, new_dir)`**: Update the snake's direction. **Crucial**: Prevent "180-degree" turns (e.g., if moving UP, the snake cannot immediately turn DOWN).
- **`move_snake(state)`**: 
  1. Calculate the new head position.
  2. Check for collisions with walls or the snake's own body.
  3. If food is eaten: Increment score and call `place_food()`.
  4. If no food is eaten: Remove the last segment of the tail.
  5. Add the new head position to the front of the body lists.

#### Step 3: Rendering Engine
Create a `render` function that uses the `tkinter.Canvas` to draw:
- The food (red rectangle).
- The snake body (green/cyan rectangles).
- The current score.
- A "GAME OVER" overlay when `alive` is False.

---

### 3. AI and Input Helpers (`snake_helpers.py`)

#### Step 1: Keyboard Handling
Create a function `make_handler` that returns a callback for `root.bind("<KeyPress>", ...)`. This handler should:
- Update the `next_dir` variable based on arrow keys.
- Set flags for restart ('R'), quit ('Q'), and auto-mode toggle ('A').

#### Step 2: AI Logic (BFS Algorithm)
Implement `bfs_next_dir(state)` to find the shortest path to the food:
- **Obstacles**: Treat all snake body segments (except the tail) as walls.
- **Queue**: Use `collections.deque` to perform a Breadth-First Search.
- **Traversal**: Explore all four directions. Store the first direction taken to reach a cell.
- **Goal**: If the food position is reached, return that first direction.
- **Fallback**: If no path is found, return -1 (continue straight).

---

### 4. The Main Game Loop (`snake_game.py`)

1. **Window Setup**: Initialize `tk.Tk()`, create a `Canvas`, and bind the keyboard handler.
2. **Game Loop**: Use a `while True` loop to repeatedly perform the following:
   - Check for input flags (Restart, Quit, Auto-mode toggle).
   - If `alive` is True:
     - In **Auto Mode**: Call `bfs_next_dir()` to set the direction.
     - In **Manual Mode**: Apply the `next_dir` captured by the keyboard.
     - Call `move_snake()`.
   - Call `render()` to update the canvas.
   - Use `root.update()` to process UI events.
   - Implement a frame delay using `time.sleep()` (e.g., 120ms for manual, 50ms for AI).

---

## 🏃 How to Run

1. Save the files in a folder.
2. Run the main script:
   ```bash
   python snake_game.py
   ```
3. **Controls**:
   - Use **Arrow Keys** to steer.
   - Press **A** to enable AI mode.
   - Press **R** to restart after death.
   - Press **Q** to quit.

---

## 📚 Key Concepts Demonstrated

- **Game Loop Architecture**: Managing state $\rightarrow$ updating logic $\rightarrow$ rendering visuals.
- **Coordinate Geometry**: Using a grid system for movement and collision detection.
- **BFS (Breadth-First Search)**: Finding the shortest path in an unweighted grid.
- **Event-Driven Programming**: Handling asynchronous keyboard inputs in a GUI.
- **Time Management**: Controlling game speed through sleep intervals.
- **State Machines**: Managing transitions between "Alive", "Game Over", and "AI Mode".
