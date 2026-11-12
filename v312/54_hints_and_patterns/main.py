# Author: Ahmet Aksoy & Claude
# Date: 12.11.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - runs on Python 3.10+; section 3 uses mypy 2.4.1 and pyright 1.1.414 if installed

"""
Type hints and match patterns that contradict their own claims.

Projects 23 (structural pattern matching) and 24 (advanced type hinting) were
written by an AI assistant. Both run and print the expected demo output.
This script shows what the type hints and patterns promise, what Python does
at runtime, and what a type checker can and cannot see.

  says   = original code from projects 23 and 24 (copied unchanged, prints removed)
  checks = corrected code

Sections:
  1. Type hints do not run: project 24 accepts what its hints forbid
  2. match patterns at runtime: an int amount is not a float, True is an int
  3. What mypy (--strict) and pyright (default mode) see in small snippets
"""

import json
import math
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

# --- says: project 24 (unchanged except for the type alias, so it runs on 3.10) ---
Identifier = int | str


class APIResponse:  # original: class APIResponse[T]  (PEP 695, Python 3.12+)
    def __init__(self, status, data, error=None):
        self.status = status
        self.data = data
        self.error = error

    def is_successful(self):
        return self.status == "success"


@dataclass
class User:
    id: Identifier
    username: str
    email: str


def process_user_response(response):
    if response.is_successful():
        user = response.data
        return f"Success: Processing User #{user.id} -> {user.username} ({user.email})"
    return f"Error occurred: {response.error}"


# --- says: project 23 -----------------------------------------------------------
@dataclass
class Order:
    product_name: str
    quantity: int
    status: str


def says_process_command(command):
    match command:
        case "EXIT":
            return "Exiting system..."
        case ["add", str(item), int(qty)]:
            return f"Stock updated: Added {qty} units of '{item}'."
        case ["delete", *id_list] if len(id_list) > 0:
            return f"Deleting products with IDs: {id_list}"
        case Order(product_name=name, quantity=qty, status="shipped"):
            return f"In-Transit: {name} ({qty} units) is currently with the carrier."
        case Order() as order:
            return f"General Order Info: {order.product_name} - Status: {order.status}"
        case {"type": "invoice", "amount": float(amt)}:
            return f"Invoice processed. Amount: ${amt:.2f}"
        case _:
            return f"Invalid or unrecognized command format: {command}"


# --- checks: project 23 -----------------------------------------------------------
def checks_process_command(command: object) -> str:
    match command:
        case "EXIT":
            return "Exiting system..."
        # bool is a subclass of int: True would match int(qty) below
        case ["add", str(), bool()]:
            return "Rejected: quantity must be a number, not True/False"
        case ["add", str(item), int(qty)] if qty > 0:
            return f"Stock updated: Added {qty} units of '{item}'."
        case ["add", *_]:
            return "Rejected: use ['add', name, quantity > 0]"
        case ["delete", *id_list] if id_list and all(type(i) is int for i in id_list):
            return f"Deleting products with IDs: {id_list}"
        case Order(product_name=name, quantity=qty, status="shipped"):
            return f"In-Transit: {name} ({qty} units) is currently with the carrier."
        case Order() as order:
            return f"General Order Info: {order.product_name} - Status: {order.status}"
        case {"type": "invoice", "amount": bool()}:
            return "Rejected: amount must be a number, not True/False"
        # JSON has one number type: 1250 arrives as int, 1250.5 as float
        case {"type": "invoice", "amount": int() | float() as amt} if amt >= 0 and math.isfinite(amt):
            return f"Invoice processed. Amount: ${amt:.2f}"
        case _:
            return f"Invalid or unrecognized command format: {command}"


# --- section 3: snippets for the type checkers -----------------------------------
SNIPPETS = {
    "a_none_data": '''
class APIResponse[T]:
    def __init__(self, status: str, data: T, error: str | None = None) -> None:
        self.status, self.data, self.error = status, data, error

class User: ...

failed: APIResponse[User] = APIResponse(status="fail", data=None, error="User not found")
''',
    "b_status_typo_str": '''
def is_successful(status: str) -> bool:
    return status == "success"

is_successful("Success")
''',
    "c_status_typo_literal": '''
from typing import Literal

def is_successful(status: Literal["success", "fail"]) -> bool:
    return status == "success"

is_successful("Success")
''',
    "d_optional_data": '''
class APIResponse[T]:
    def __init__(self, status: str, data: T | None = None) -> None:
        self.status, self.data = status, data

    def is_successful(self) -> bool:
        return self.status == "success"

def name(r: APIResponse[str]) -> str:
    if r.is_successful():
        return r.data.upper()
    return "error"
''',
    "e_result_union": '''
from dataclasses import dataclass

@dataclass
class Ok[T]:
    data: T

@dataclass
class Err:
    error: str

type Result[T] = Ok[T] | Err

def name(r: Result[str]) -> str:
    match r:
        case Ok(data=d):
            return d.upper()
        case Err(error=e):
            return e
''',
    "f_forgotten_case": '''
from dataclasses import dataclass
from typing import assert_never

@dataclass
class Add:
    qty: int

@dataclass
class Exit:
    pass

type Command = Add | Exit

def run(cmd: Command) -> str:
    match cmd:
        case Add(qty=q):
            return f"add {q}"
        case _:
            assert_never(cmd)
''',
    "g_float_pattern": '''
from typing import assert_never

def kind(x: float) -> str:
    match x:
        case float():
            return "float"
        case _:
            assert_never(x)

kind(1250)
''',
    "h_mapping_pattern": '''
from typing import Literal, TypedDict, assert_never

class Invoice(TypedDict):
    type: Literal["invoice"]
    amount: float

def handle(inv: Invoice) -> str:
    match inv:
        case {"type": "invoice", "amount": int() | float() as amt}:
            return f"{amt:.2f}"
        case _:
            assert_never(inv)
''',
    "i_bool_as_int": '''
def add(item: str, qty: int) -> str:
    return f"{qty} x {item}"

add("Laptop", True)
''',
    "j_mixed_generic_list": '''
from dataclasses import dataclass

@dataclass(frozen=True)
class APIResponse[T]:
    data: T | None = None

    @classmethod
    def ok(cls, data: T) -> "APIResponse[T]":  # T as a parameter: the class becomes invariant
        return cls(data)

def describe[T](r: APIResponse[T]) -> str:
    return str(r.data)

responses: list[APIResponse[int] | APIResponse[str]] = [APIResponse(1), APIResponse("a")]
for r in responses:
    describe(r)
''',
}


def first_error(tool, path):
    """Return 'ok' or 'error [code]' for the first error the tool reports."""
    if tool == "mypy":
        cmd = [sys.executable, "-m", "mypy", "--strict", "--python-version", "3.12",
               "--no-error-summary", "--no-color-output", "--hide-error-context", str(path)]
        out = subprocess.run(cmd, check=False, capture_output=True, text=True).stdout
        for line in out.splitlines():
            if ": error: " in line:
                return "error [" + line.rsplit("[", 1)[-1]
        return "ok"
    cmd = [shutil.which("pyright") or "pyright", "--outputjson", "--pythonversion", "3.12", str(path)]
    out = subprocess.run(cmd, check=False, capture_output=True, text=True).stdout
    for diag in json.loads(out)["generalDiagnostics"]:
        if diag["severity"] == "error":
            return f"error [{diag.get('rule', '')}]"
    return "ok"


def have(tool):
    if tool == "mypy":
        return subprocess.run([sys.executable, "-m", "mypy", "--version"], check=False, capture_output=True).returncode == 0
    return shutil.which("pyright") is not None


def main():
    print(f"Python {sys.version.split()[0]}")

    print("\n== 1. Type hints do not run (project 24) ==")
    label = "User(id=3.5, username=None, email=42)"
    print(f"  {label:44} -> {User(id=3.5, username=None, email=42)}")
    r = APIResponse(status="success", data=None)
    try:
        result = process_user_response(r)
    except AttributeError as e:
        result = f"AttributeError: {e}"
    label = 'APIResponse(status="success", data=None)'
    print(f"  {label:44} -> {result}")
    r = APIResponse(status="Success", data=User(1, "ahmet", "a@example.com"))
    label = 'APIResponse(status="Success", data=User(...))'
    print(f"  {label:44} -> {process_user_response(r)}")

    print("\n== 2. match patterns at runtime (project 23) ==")
    inputs = [
        {"type": "invoice", "amount": 1250.5},
        {"type": "invoice", "amount": 1250},
        {"type": "invoice", "amount": True},
        ["add", "Laptop", 2],
        ["add", "Laptop", True],
        ["add", "Laptop", -3],
        ["delete", True, False],
    ]
    for x in inputs:
        print(f"  {x!s}")
        print(f"    says     {says_process_command(x)}")
        print(f"    checks   {checks_process_command(x)}")

    print("\n== 3. What mypy (--strict) and pyright (default mode) see ==")
    tools = [t for t in ("mypy", "pyright") if have(t)]
    if not tools:
        print("  skipped: pip install mypy pyright")
        return
    print(f"  {'snippet':24}" + "".join(f"{t:34}" for t in tools))
    with tempfile.TemporaryDirectory() as tmp:
        for name, code in SNIPPETS.items():
            path = Path(tmp) / f"{name}.py"
            path.write_text(code.lstrip())
            print(f"  {name:24}" + "".join(f"{first_error(t, path):34}" for t in tools))


if __name__ == "__main__":
    main()
