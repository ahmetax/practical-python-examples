# Project 33: Unit Testing with pytest

A small example of unit testing with `pytest`. The code under test and the tests live in separate files:

| File | Contents |
|------|----------|
| `math_operations.py` | `divide_numbers()` raises `ValueError` when the denominator is zero; `calculate_average()` returns `0.0` for an empty list |
| `test_math_operations.py` | Five tests: normal results, the error case and edge cases (empty list, single element) |

## How It Works
- pytest finds tests by name: files that start with `test_` and functions inside them that start with `test_`.
- The tests use plain `assert` statements; pytest shows the compared values when an assertion fails.
- `pytest.raises(ValueError)` checks that dividing by zero raises the expected exception. The test also compares the error message (`str(exc_info.value)`).
- `math_operations.py` has no `if __name__ == "__main__":` block, so running it with `python3` prints nothing. The project is run through pytest.

## Project Structure
```text
33_unit_testing/
├── math_operations.py
├── test_math_operations.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (pytest 9 requires 3.10+; the code itself uses `list[float]`, which needs 3.9). Tested on 3.12.3.
- Third-party package: `pytest`. Tested with pytest 9.1.1.

## Running
Run the commands inside the `33_unit_testing` folder:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -v
```
`-v` (verbose) lists every test with its result.

## Sample Output (Python 3.12.3)
```text
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /path/to/.venv/bin/python3
rootdir: /path/to/33_unit_testing
collecting ... collected 5 items

test_math_operations.py::test_divide_numbers_success PASSED              [ 20%]
test_math_operations.py::test_divide_numbers_by_zero PASSED              [ 40%]
test_math_operations.py::test_calculate_average_normal_list PASSED       [ 60%]
test_math_operations.py::test_calculate_average_empty_list PASSED        [ 80%]
test_math_operations.py::test_calculate_average_single_element PASSED    [100%]

============================== 5 passed in 0.03s ===============================
```
Paths and the run time differ on your machine. pytest creates `.pytest_cache/` and `__pycache__/` folders in the project; you can delete them safely.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/09/05/pythonda-kodunuzu-kirilmaktan-koruyun-pytest-ile-birim-testi-yazmak/
- pytest documentation: https://docs.pytest.org/
