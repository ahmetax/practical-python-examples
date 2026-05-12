# Hello World Project (Claude Code Edition)

A minimal Python project demonstrating a basic "Hello World" implementation. This README is designed as a specification for Claude Code to generate this project from scratch.

## Project Overview
The goal of this project is to create a single Python script that outputs a greeting to the standard output.

## Specifications for Claude Code

If you are asking Claude Code to recreate this project, you can use the following prompt:

> "Create a directory named `01_hello_world`. Inside it, create a Python file `hello_world.py` that prints 'Hello World!'. Include a header docstring with Author: Ahmet Aksoy, Date: 2026-04-16, and Environment: Python 3.12 - Ubuntu 24.04."

## Project Structure
```
01_hello_world/
└── hello_world.py    # Main execution script
```

## Implementation Details

### `hello_world.py`
- **Purpose**: Print "Hello World!" to the console.
- **Requirements**: 
    - Python 3.12
    - Standard library only (no external dependencies).
    - Must include metadata in the top-level docstring.

## Setup and Execution Instructions

### 1. Environment Setup
Ensure you have Python 3.12 installed.

### 2. Running the Project
From the root of the project directory, execute:
```bash
python3 hello_world.py
```

## Expected Result
The terminal should display:
```text
Hello World!
```
