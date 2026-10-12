# Project 24: Type Hints and Generics with the Python 3.12 Syntax

A short example of the type parameter syntax introduced in Python 3.12 (PEP 695). The code defines a type alias with the `type` statement and a generic class with `class APIResponse[T]:`, without declaring a `TypeVar`. Two dataclasses (`User`, `Product`) are wrapped in `APIResponse`, and the handler functions declare exactly which kind of response they accept.

| # | Topic | Example in the code |
|---|-------|---------------------|
| 1 | Type alias (PEP 695) | `type Identifier = int \| str` |
| 2 | Generic class without `TypeVar` (PEP 695) | `class APIResponse[T]:` |
| 3 | Union with `\|` and optional values | `error: str \| None = None` |
| 4 | Parameterised generic in a signature | `def process_user_response(response: APIResponse[User]) -> None:` |

## Project Structure
```text
24_advanced_type_hinting/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.12 or newer. The `type` statement and the `class Name[T]:` syntax do not exist before 3.12; on 3.11 the file fails with `SyntaxError: invalid syntax` at `type Identifier = int | str`. Tested on 3.12.3.
- No third-party packages. `mypy` is optional, only for the type check below.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Advanced Type Hinting Test Started ---

Success: Processing User #101 -> ahmet_dev (ahmet@example.com)
--------------------------------------------------
Success: Processing Product #PROD-99X -> Mechanical Keyboard costs $89.99
--------------------------------------------------
Error occurred: User not found
```

## Checking With mypy
Type hints are not enforced at run time; a static type checker reads them. To try it:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mypy
mypy main.py
```
With mypy 2.4.0 the result is:
```text
main.py:88: error: Argument "data" to "APIResponse" has incompatible type "None"; expected "User"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```
The failed-response example passes `data=None` to an `APIResponse[User]`, but `data` is declared as `T`, not `T | None`. Python runs it without complaint; mypy reports it. Changing the parameter to `data: T | None` (and handling `None` in the handlers) would remove the error.

## How It Works
- `type Identifier = int | str` creates a lazily evaluated type alias; `User.id` and `Product.id` can be either an integer or a string.
- `class APIResponse[T]:` declares the type parameter `T` directly in the class header. mypy infers `APIResponse[User]` from `APIResponse(status="success", data=user_data)`, so `response.data` is known to be a `User`.
- `process_user_response()` accepts only `APIResponse[User]`; passing an `APIResponse[Product]` would be a type error for mypy, but not at run time.
- The file still imports `Generic` and `TypeVar` from `typing` (line 11), but does not use them; the new syntax makes them unnecessary here.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/05/python-3-12-ile-tip-sisteminde-yeni-bir-donem-pep-695-ve-gelismis-jenerikler/
- PEP 695: Type Parameter Syntax: https://peps.python.org/pep-0695/
- `typing` documentation: https://docs.python.org/3/library/typing.html
