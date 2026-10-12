# Project 23: Structural Pattern Matching (match-case)

A small command processor that uses `match`/`case` instead of an `if`/`elif` chain. The `process_command()` function receives inputs of different shapes (a string, lists, `Order` dataclass objects, a dictionary) and picks a branch based on the structure and types of the input.

| # | Pattern type | Example in the code |
|---|--------------|---------------------|
| 1 | Literal pattern | `case "EXIT":` |
| 2 | Sequence pattern with type checks | `case ["add", str(item), int(qty)]:` |
| 3 | Star pattern with a guard | `case ["delete", *id_list] if len(id_list) > 0:` |
| 4 | Class pattern (keyword attributes) | `case Order(product_name=name, quantity=qty, status="shipped"):` |
| 5 | Class pattern with `as` binding | `case Order() as order:` |
| 6 | Mapping pattern | `case {"type": "invoice", "amount": float(amt)}:` |
| 7 | Wildcard | `case _:` |

## Project Structure
```text
23_structural_pattern_matching/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.10 or newer (`match`/`case` was added in 3.10, PEP 634). Tested on 3.12.3; also runs on 3.10 and 3.11.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Python Match-Case Test Started ---

Input: ['add', 'Laptop', 2]
Stock updated: Added 2 units of 'Laptop'.
---------------------------------------------
Input: ['delete', 404, 505]
Deleting products with IDs: [404, 505]
---------------------------------------------
Input: Order(product_name='Wireless Headphones', quantity=1, status='shipped')
In-Transit: Wireless Headphones (1 units) is currently with the carrier.
---------------------------------------------
Input: Order(product_name='Coffee Maker', quantity=1, status='pending')
General Order Info: Coffee Maker - Status: pending
---------------------------------------------
Input: {'type': 'invoice', 'amount': 1250.5}
Invoice processed. Amount: $1250.50
---------------------------------------------
Input: ['invalid_command_format']
Invalid or unrecognized command format: ['invalid_command_format']
---------------------------------------------
Input: EXIT
Exiting system...
---------------------------------------------
```

## How It Works
- The `case` blocks are tried from top to bottom; the first one that matches runs. That is why `Order(..., status="shipped")` comes before the general `Order()` case.
- `str(item)` and `int(qty)` check the type and bind the value at the same time. `["add", "Laptop", "2"]` (quantity as a string) does not match and falls through to `case _`.
- A sequence pattern matches lists and tuples, but never strings. `("add", "Laptop", 2)` matches the `add` case as well.
- `*id_list` collects the remaining elements; the guard `if len(id_list) > 0` rejects a bare `["delete"]`.
- The mapping pattern only checks the listed keys; extra keys are ignored. Because of `float(amt)`, an integer amount such as `{"type": "invoice", "amount": 1250}` does not match.
- `process_command()` returns `False` only for `"EXIT"`, which stops the loop.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/02/pythonda-modern-veri-ayristirma-yapisal-pattern-matching-match-case/
- The `match` statement: https://docs.python.org/3/reference/compound_stmts.html#the-match-statement
- PEP 636: Structural Pattern Matching tutorial: https://peps.python.org/pep-0636/
