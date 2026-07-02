# Project 33: Automated Unit Testing with Pytest

A production-ready testing example demonstrating how to isolate business logic and implement automated test execution suites using `pytest`. This project covers basic assertions, checking edge cases, and verifying expected exception states.

## Architectural Goal
The application establishes a formal test-driven layer within the code repository. By decoupling execution functions from the testing scripts, it allows continuous integration (CI) runners or pre-commit hooks to automatically parse execution states, ensuring that incoming changes do not introduce regressions into established business domains.

## Project Structure
```text
33_unit_testing/
├── math_operations.py
└── test_math_operations.py

System Requirements
- OS: Ubuntu 24.04 (or any Linux/UNIX-compatible system)
- Runtime: Python 3.12+

Setup & Dependencies
Pytest is an external framework package that needs to be installed inside your virtual environment. Run the following command:

```bash
pip install pytest

How to Recreate This Project From Scratch
Step 1: Directory Setup
Create a dedicated folder for this project inside your repository workspace:

```bash
mkdir 33_unit_testing
cd 33_unit_testing

### Step 2: Implement Core Functions and Test Suits
1. Create the Target Module: Create a file named math_operations.py. Inside, implement core utility tasks like a division function (divide_numbers) that explicitly guards boundaries by raising a ValueError during division-by-zero attempts, and an array calculation function (calculate_average) that safely manages empty inputs.

2. Create the Testing Module: Create a file named test_math_operations.py. Note: Pytest depends on naming conventions to automatically discover tests; your file name must start with test_ and your interior test functions must also start with the test_ prefix.

3. Draft Target Verifications: Implement clear test blocks using plain Python assert statements.

  - Write standard path evaluations (e.g., verifying divide_numbers(10, 2) == 5.0).

  - Use the with pytest.raises(ValueError): context manager block to verify that your system components actively intercept and raise expected exceptions on forbidden input parameters.

### Step 3: Run and Verify
Instead of running Python directly on the script, invoke the pytest engine from your terminal inside the project directory:

```bash
pytest -v

The -v (verbose) flag commands the runner to list out every test scenario alongside its matching verification state, outputting a clean green pass summary profile.


