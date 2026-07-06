# Project 34: Modern Package Management with Poetry

A production-grade example demonstrating how to manage Python third-party dependencies, sub-dependency resolution isolation, and virtual environments using the modern industrial standard, `Poetry`. This project completely replaces traditional legacy workflows like `pip` and `requirements.txt`.

## Architectural Goal
The system introduces a deterministic blueprint design to dependency resolution. By replacing loosely mapped requirements sheets with strict, reproducible lock manifests (`poetry.lock`), it guarantees that exact software component trees are replicated identically across all local developer machines, staging clusters, and automated continuous deployment (CD) workflows.

## Project Structure
```text
34_poetry_package_management/
├── pyproject.toml
└── src/
    └── main.py

## System Requirements
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)
- Runtime: Python 3.12+
- Global Dependency: Poetry engine installed globally or user-wide on your system.

## Setting Up Poetry on Ubuntu
If you do not have Poetry installed on your host system, install it using the official standard installation script:

```bash
curl -sSL https://install.python-poetry.org | python3 -

Verify the installation by checking the version footprint:

```bash
poetry --version

## How to Recreate This Project From Scratch
### Step 1: Directory and Package Initialisation
Create a dedicated folder for this project inside your repository workspace:

```bash
mkdir 34_poetry_package_management
cd 34_poetry_package_management

Instead of writing configuration schemas manually, you can initialize a standard layout natively via:

```bash
poetry init --no-interaction

This generates your fundamental structure mapping blueprint, pyproject.toml.

### Step 2: Configuring Dependencies and Source Code
- Define the pyproject.toml Layout: Ensure your pyproject.toml lists target constraints, including specific runtime platforms (e.g., python = "^3.12"), core packages (like requests and rich), and isolated developer groups (pytest).

- Add Dependencies Programmatically: Instead of editing raw files, add libraries using Poetry's interactive CLI. This triggers immediate cryptographic calculation checks and resolves sub-dependency graphs cleanly:

```bash
poetry add rich requests
poetry add pytest --group dev

- Draft the Implementation Entrypoint: Create a src/ directory and add main.py. Import your newly managed dependencies—such as rich.table—to verify that your code can cleanly tap into isolated package structures at runtime.

### Step 3: Run and Verify
Poetry isolates all dependencies inside a dedicated virtual environment layer. To execute the application code inside this protected context, use the poetry run command wrapper:

```bash
poetry run python3 src/main.py

This activates the runtime layer seamlessly on the fly and outputs a beautifully formatted system visualization matrix inside your Ubuntu CLI interface.


---

