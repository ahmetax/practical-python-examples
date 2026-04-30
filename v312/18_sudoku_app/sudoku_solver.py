"""
Python Sudoku Solver — subprocess olarak çağrılır.

Kullanım:
  python sudoku_solver.py <81-char-puzzle-string>

Çıktı:
  {"solution":"<81-char>","elapsed_ns":<int>,"solved":<bool>}
"""

import sys
import time


# ------------------------------------------------------------------ #
# Board helpers
# ------------------------------------------------------------------ #

def make_board(flat: str) -> list[list[int]]:
    """Parse 81-char string into 9x9 board."""
    board = []
    for r in range(9):
        row = []
        for c in range(9):
            idx = r * 9 + c
            val = int(flat[idx])
            row.append(val)
        board.append(row)
    return board


def board_to_flat(board: list[list[int]]) -> str:
    """Convert 9x9 board to 81-char string."""
    result = ""
    for r in range(9):
        for c in range(9):
            result += str(board[r][c])
    return result


def copy_board(src: list[list[int]]) -> list[list[int]]:
    """Deep copy a 9x9 board."""
    dst = []
    for r in range(9):
        row = []
        for c in range(9):
            row.append(src[r][c])
        dst.append(row)
    return dst


# ------------------------------------------------------------------ #
# Validator
# ------------------------------------------------------------------ #

def is_valid(board: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if num can be placed at board[row][col]."""
    for c in range(9):
        if board[row][c] == num:
            return False
    for r in range(9):
        if board[r][col] == num:
            return False
    box_r = (row // 3) * 3
    box_c = (col // 3) * 3
    for r in range(box_r, box_r + 3):
        for c in range(box_c, box_c + 3):
            if board[r][c] == num:
                return False
    return True


# ------------------------------------------------------------------ #
# find_empty — tuple dönemiyor, row/col ayrı out parametresi
# ------------------------------------------------------------------ #

def find_empty_row(board: list[list[int]]) -> int:
    """Return row of first empty cell, or -1 if none."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r
    return -1


def find_empty_col(board: list[list[int]]) -> int:
    """Return col of first empty cell, or -1 if none."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return c
    return -1


# ------------------------------------------------------------------ #
# Solver — backtracking
# ------------------------------------------------------------------ #

def solve(board: list[list[int]]) -> bool:
    """Solve in-place using backtracking. Returns True if solved."""
    row = find_empty_row(board)
    col = find_empty_col(board)

    if row == -1:
        return True   # no empty cell — solved

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0

    return False


# ------------------------------------------------------------------ #
# Main
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print('{"error":"Missing puzzle argument","solved":false}')
        sys.exit(1)

    flat = argv[1]
    if len(flat) != 81:
        print('{"error":"Puzzle must be 81 characters","solved":false}')
        sys.exit(1)

    board = make_board(flat)
    t0 = time.perf_counter_ns()
    solved = solve(board)
    elapsed = time.perf_counter_ns() - t0

    solution = board_to_flat(board) if solved else flat

    print(
        '{"solution":"' + solution + '"' +
        ',"elapsed_ns":' + str(elapsed) +
        ',"solved":' + ("true" if solved else "false") +
        '}'
    )