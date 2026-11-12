# Project 54: Type Hints Don't Run, Patterns Mislead — What mypy and pyright See in AI-Written Code

Projects 23 (structural pattern matching) and 24 (advanced type hinting) were written by an AI assistant. Both run and print the expected demo output. Project 24's comments say mypy "will know exactly" what the types are; mypy does, and reports an error in that very file. This script shows what the hints and patterns promise, what Python does at runtime, and what the type checkers can and cannot see.

| Problem | Example | mypy --strict | pyright |
|---|---|---|---|
| `data=None` for `data: T` (project 24) | `APIResponse(status="fail", data=None)` | error | error |
| Status typo, `status: str` | `is_successful("Success")` | ok | ok |
| Forgotten `case` in a dataclass union | `assert_never(cmd)` | error | error |
| `case float()` on a `float` value | `kind(1250)` | ok (misses it) | error |
| Mapping pattern on a `TypedDict` | `assert_never(inv)` | error even when correct | error even when correct |
| `True` as an `int` | `add("Laptop", True)` | ok | ok |

## How It Works
- Section 1 runs project 24's `User` and `APIResponse` with values the hints forbid. Python accepts all of them; the failure, if any, appears later.
- Section 2 runs project 23's `process_command` ("says") and a corrected version ("checks"). `float(amt)` is an `isinstance` check, so a JSON amount of `1250` (an `int`) is rejected; `int(qty)` matches `True` because `bool` is a subclass of `int`. The corrected version matches `bool()` first, uses `int() | float()` with a guard, and checks IDs with `type(i) is int`.
- Section 3 writes ten small snippets to a temporary directory and runs `mypy --strict --python-version 3.12` and `pyright --pythonversion 3.12` on each, printing the first error code. It is skipped if neither tool is installed.
- Snippet `d` is the obvious fix for project 24 (`data: T | None`): `is_successful()` does not narrow the type, so both checkers flag `r.data.upper()`. Snippet `e` (`Ok[T] | Err` with `match`) passes both.
- Snippet `j` reproduces the error in four of five versions of project 24 that Claude wrote on 12.11.2026: with PEP 695, variance is inferred, and a method that takes `T` as a parameter (`ok(cls, data: T)`) makes the class invariant, so a list mixing `APIResponse[int]` and `APIResponse[str]` cannot be passed to `describe[T]`.

## Project Structure
```text
54_hints_and_patterns/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer. Tested on 3.12.3 and in Docker on 3.10 and 3.14 (sections 1 and 2 identical).
- Sections 1 and 2 need no third-party packages. Section 3 needs `mypy` and/or `pyright` (tested with mypy 2.4.1 and pyright 1.1.414; other versions may report different codes).

## Running
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mypy pyright
python3 main.py
```
pyright may download its own Node.js runtime on first use.

## Sample Output (Python 3.12.3)
```text
Python 3.12.3

== 1. Type hints do not run (project 24) ==
  User(id=3.5, username=None, email=42)        -> User(id=3.5, username=None, email=42)
  APIResponse(status="success", data=None)     -> AttributeError: 'NoneType' object has no attribute 'id'
  APIResponse(status="Success", data=User(...)) -> Error occurred: None

== 2. match patterns at runtime (project 23) ==
  {'type': 'invoice', 'amount': 1250.5}
    says     Invoice processed. Amount: $1250.50
    checks   Invoice processed. Amount: $1250.50
  {'type': 'invoice', 'amount': 1250}
    says     Invalid or unrecognized command format: {'type': 'invoice', 'amount': 1250}
    checks   Invoice processed. Amount: $1250.00
  {'type': 'invoice', 'amount': True}
    says     Invalid or unrecognized command format: {'type': 'invoice', 'amount': True}
    checks   Rejected: amount must be a number, not True/False
  ['add', 'Laptop', 2]
    says     Stock updated: Added 2 units of 'Laptop'.
    checks   Stock updated: Added 2 units of 'Laptop'.
  ['add', 'Laptop', True]
    says     Stock updated: Added True units of 'Laptop'.
    checks   Rejected: quantity must be a number, not True/False
  ['add', 'Laptop', -3]
    says     Stock updated: Added -3 units of 'Laptop'.
    checks   Rejected: use ['add', name, quantity > 0]
  ['delete', True, False]
    says     Deleting products with IDs: [True, False]
    checks   Invalid or unrecognized command format: ['delete', True, False]

== 3. What mypy (--strict) and pyright (default mode) see ==
  snippet                 mypy                              pyright                           
  a_none_data             error [arg-type]                  error [reportAssignmentType]      
  b_status_typo_str       ok                                ok                                
  c_status_typo_literal   error [arg-type]                  error [reportArgumentType]        
  d_optional_data         error [union-attr]                error [reportOptionalMemberAccess]
  e_result_union          ok                                ok                                
  f_forgotten_case        error [arg-type]                  error [reportArgumentType]        
  g_float_pattern         ok                                error [reportArgumentType]        
  h_mapping_pattern       error [arg-type]                  error [reportArgumentType]        
  i_bool_as_int           ok                                ok                                
  j_mixed_generic_list    error [misc]                      error [reportArgumentType]        
```

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/30/tip-ipuclari-calismaz-desenler-yanilir-mypy-pyright/
- Original projects: `v312/23_structural_pattern_matching`, `v312/24_advanced_type_hinting`
- PEP 695, variance inference: https://peps.python.org/pep-0695/#variance-inference
- PEP 634, structural pattern matching: https://peps.python.org/pep-0634/
- typing.assert_never: https://docs.python.org/3/library/typing.html#typing.assert_never
