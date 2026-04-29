"""
Author: Ahmet Aksoy
Date: 2026-04-27
Python 3.12 - Ubuntu 24.04

Description:
    Classic Snake game implemented in Python using tkinter library.

    Game state is stored in a Python dict to manage all mutable state.

    The game logic (movement, collision, food placement, scoring) is
    implemented in Python functions. The graphical interface (window,
    canvas, keyboard input) is handled by tkinter.

    Controls:
      Arrow keys — change direction
      R          — restart after game over
      Q          — quit
      A          — auto mode on/off

    Rules:
      - Snake grows by 1 segment each time it eats food.
      - Game ends if the snake hits a wall or its own body.
      - Score increases by 10 for each food eaten.

Requirements:
    tkinter is included in Python's standard library.
    No additional packages needed.
"""

import tkinter as tk
import time
import random
import snake_helpers

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3


def make_state(grid_w, grid_h):
    """
    Create and return the initial game state as a Python dict.

    Keys:
      body_x, body_y : Python lists of Int — snake segments, head at index 0
      dir            : current direction (DIR_* constant)
      dx, dy         : movement delta per step
      score          : current score
      alive          : True while game is running
      food_x, food_y : current food position
      grid_w, grid_h : grid dimensions
    """
    cx = grid_w // 2
    cy = grid_h // 2

    bx = [cx, cx - 1, cx - 2]
    by = [cy, cy, cy]

    s = {
        "body_x": bx,
        "body_y": by,
        "dir": DIR_RIGHT,
        "dx": 1,
        "dy": 0,
        "score": 0,
        "alive": True,
        "grid_w": grid_w,
        "grid_h": grid_h,
        "food_x": 0,
        "food_y": 0
    }
    place_food(s)
    return s


def place_food(s):
    """Place food at a random unoccupied cell."""
    grid_w = s["grid_w"]
    grid_h = s["grid_h"]
    n = len(s["body_x"])

    while True:
        fx = random.randint(0, grid_w - 1)
        fy = random.randint(0, grid_h - 1)
        occupied = False
        for i in range(n):
            bx = s["body_x"][i]
            by = s["body_y"][i]
            if bx == fx and by == fy:
                occupied = True
                break
        if not occupied:
            s["food_x"] = fx
            s["food_y"] = fy
            break


def set_direction(s, new_dir):
    """Update direction, ignoring 180-degree reversals."""
    cur = s["dir"]

    if new_dir == DIR_UP and cur != DIR_DOWN:
        s["dir"] = DIR_UP; s["dx"] = 0; s["dy"] = -1
    elif new_dir == DIR_DOWN and cur != DIR_UP:
        s["dir"] = DIR_DOWN; s["dx"] = 0; s["dy"] = 1
    elif new_dir == DIR_LEFT and cur != DIR_RIGHT:
        s["dir"] = DIR_LEFT; s["dx"] = -1; s["dy"] = 0
    elif new_dir == DIR_RIGHT and cur != DIR_LEFT:
        s["dir"] = DIR_RIGHT; s["dx"] = 1; s["dy"] = 0


def move_snake(s):
    """
    Advance the snake one step.
    Updates body, score, alive, and food in the state dict.
    """
    dx = s["dx"]
    dy = s["dy"]
    head_x = s["body_x"][0]
    head_y = s["body_y"][0]
    grid_w = s["grid_w"]
    grid_h = s["grid_h"]
    food_x = s["food_x"]
    food_y = s["food_y"]

    new_x = head_x + dx
    new_y = head_y + dy

    # Wall collision
    if new_x < 0 or new_x >= grid_w or new_y < 0 or new_y >= grid_h:
        s["alive"] = False
        return

    # Self collision
    n = len(s["body_x"])
    for i in range(n):
        bx = s["body_x"][i]
        by = s["body_y"][i]
        if bx == new_x and by == new_y:
            s["alive"] = False
            return

    # Insert new head
    s["body_x"].insert(0, new_x)
    s["body_y"].insert(0, new_y)

    # Food check
    if new_x == food_x and new_y == food_y:
        s["score"] += 10
        place_food(s)
    else:
        # Remove tail
        s["body_x"].pop()
        s["body_y"].pop()


def draw_cell(canvas, x, y, color, cell):
    """Draw one grid cell as a filled rectangle."""
    x1 = x * cell
    y1 = y * cell
    canvas.create_rectangle(
        x1, y1, x1 + cell, y1 + cell,
        fill=color, outline="#222222"
    )


def render(canvas, s, cell, win_w, win_h, auto_mode):
    """Clear canvas and redraw all game elements."""
    canvas.delete("all")

    food_x = s["food_x"]
    food_y = s["food_y"]
    score = s["score"]
    alive = s["alive"]
    n = len(s["body_x"])

    # Food
    draw_cell(canvas, food_x, food_y, "#FF4444", cell)

    # Snake body — cyan head in auto mode, green in manual
    for i in range(n):
        bx = s["body_x"][i]
        by = s["body_y"][i]
        if i == 0:
            color = "#00DDFF" if auto_mode else "#00EE55"
        else:
            color = "#0099BB" if auto_mode else "#00AA33"
        draw_cell(canvas, bx, by, color, cell)

    # Score label
    canvas.create_text(
        6, 6, anchor="nw",
        text=f"Score: {score}",
        fill="white",
        font=('Arial', 12, 'bold')
    )

    # Auto mode indicator (top-right)
    if auto_mode:
        canvas.create_text(
            win_w - 6, 6, anchor="ne",
            text="AUTO  [A] to disable",
            fill="#00DDFF",
            font=('Arial', 11, 'bold')
        )
    else:
        canvas.create_text(
            win_w - 6, 6, anchor="ne",
            text="[A] Auto mode",
            fill="#888888",
            font=('Arial', 11)
        )

    # Game over overlay
    if not alive:
        canvas.create_text(
            win_w // 2, win_h // 2 - 24,
            text="GAME OVER",
            fill="#FF4444",
            font=('Arial', 30, 'bold')
        )
        canvas.create_text(
            win_w // 2, win_h // 2 + 18,
            text=f"Score: {score}    |  R = restart  |  A = auto mode  |  Q = quit",
            fill="white",
            font=('Arial', 13)
        )


def run_game():
    cell = 20
    grid_w = 30
    grid_h = 25
    win_w = cell * grid_w
    win_h = cell * grid_h
    fps_ms = 120

    # All game state in one Python dict
    s = make_state(grid_w, grid_h)

    # --- Window setup ---
    root = tk.Tk()
    root.title("Snake — Python + tkinter")
    root.resizable(False, False)
    canvas = tk.Canvas(
        root, width=win_w, height=win_h, bg="#111111"
    )
    canvas.pack()

    # Shared input state:
    # next_dir[0] : pending direction
    # flags[0]    : restart (R)
    # flags[1]    : quit (Q)
    # flags[2]    : toggle auto mode (A)
    next_dir = [3]
    flags = [False, False, False]

    key_handler = snake_helpers.make_handler(next_dir, flags)

    root.bind("<KeyPress>", key_handler)
    root.focus_set()

    auto_mode = False

    render(canvas, s, cell, win_w, win_h, auto_mode)
    root.update()

    while True:
        try:
            root.winfo_exists()
        except:
            break

        if flags[1]:
            break

        if flags[0]:
            s = make_state(grid_w, grid_h)
            flags[0] = False
            next_dir[0] = DIR_RIGHT

        # Toggle auto mode
        if flags[2]:
            auto_mode = not auto_mode
            flags[2] = False

        if s["alive"]:
            if auto_mode:
                # BFS: find best next direction
                bfs_dir = snake_helpers.bfs_next_dir(s)
                if bfs_dir >= 0:
                    set_direction(s, bfs_dir)
                # if bfs_dir == -1: no path, keep current direction
            else:
                new_dir = next_dir[0]
                set_direction(s, new_dir)
            move_snake(s)

        render(canvas, s, cell, win_w, win_h, auto_mode)

        try:
            root.update()
        except:
            break

        # Auto mode runs faster (50ms), manual mode normal (120ms)
        frame_ms = 50 if auto_mode else fps_ms
        steps = 6
        step_ms = frame_ms / steps
        for _ in range(steps):
            time.sleep(step_ms / 1000.0)
            try:
                root.update()
            except:
                break

    try:
        root.destroy()
    except:
        pass



if __name__ == "__main__":
    run_game()