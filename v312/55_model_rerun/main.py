# Author: Ahmet Aksoy & Claude
# Date: 03.12.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - runs on Python 3.9+

"""
Are the models getting better? Same task, August code vs. today's answer.

In August/September an AI assistant wrote projects 31 (merge sort), 32 (binary
search tree) and 38 (regex validators). Later posts found problems in them
that the demo inputs never showed. Here the same three tasks were given again
to today's model (Claude Code 2.1.325, claude-opus-5-5, tools off, 5 runs per
task, prompts below). This script checks the old code and one of today's
answers with the same bad inputs.

  says  = original code from projects 31, 32 and 38 (copied unchanged)
  model = one of today's five answers (regex: run 4, merge sort: run 1,
          tree: run 1). The other runs differ in details; the counts over
          all five runs are in the blog post.

Usage:
  python3 main.py                  # old code vs. the embedded answers
  python3 main.py regex file.py    # test any file (regex | sort | tree)
"""

from __future__ import annotations

import contextlib
import io
import random
import sys
import time
from dataclasses import dataclass, field

PROMPTS = {
    "regex": (
        "Write three validation functions in Python using the re module: "
        "validate_email(email) -> bool, validate_turkish_phone(phone) -> bool "
        "(accept +90, 0 prefix and spaced formats), assess_password_strength(password) "
        "-> list[str] (missing requirements: length, uppercase, lowercase, digit, special; "
        "empty list if all met). Give only the full main.py code in one python block."
    ),
    "sort": (
        "Write merge sort in Python: merge_sort(arr) takes a list and returns the elements "
        "in ascending order as a new list. Give only the full main.py code in one python block."
    ),
    "tree": (
        "Write a binary search tree in Python: class BinarySearchTree with insert(value), "
        "search(target) -> bool and get_inorder_list() -> list. Give only the full main.py "
        "code in one python block."
    ),
}
# (The real prompts were in Turkish; see the blog post.)

SAYS_REGEX = r'''
import re


def validate_email(email: str) -> bool:
    r"""
    Validates an email address layout using structural boundary tracking.
    Pattern breakdown:
    - ^[a-zA-Z0-9._%+-]+ : Starts with one or more alphanumeric/allowed special chars
    - @                  : Must contain exactly one literal '@' symbol
    - [a-zA-Z0-9.-]+     : Followed by a domain name alphanumeric segment
    - \.[a-zA-Z]{2,}$    : Concludes with a period and at least a 2-character Top-Level Domain
    """
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_pattern, email))


def validate_turkish_phone(phone: str) -> bool:
    """
    Validates Turkish phone numbers (with or without +90/0 prefixes and spaces).
    Matches formats like: +905551234567, 0555 123 45 67, 5551234567
    """
    phone_pattern = r"^(?:\+90|0)?\s?([5]\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$"
    match = re.match(phone_pattern, phone)
    
    if match:
        # Demonstrates how regex groups can extract sanitized segments from raw text
        area_code, part1, part2, part3 = match.groups()
        print(f"   [Sanitized Output] Extracted -> Area: ({area_code}) Number: {part1}-{part2}-{part3}")
        return True
    return False


def assess_password_strength(password: str) -> list[str]:
    """
    Evaluates password security thresholds using multiple targeted lookups.
    Returns a list of missing requirement statements. Secure passwords require:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one numerical digit
    - At least one special character (@$!%*?&)
    """
    failed_criteria = []
    
    if len(password) < 8:
        failed_criteria.append("Minimum length must be at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        failed_criteria.append("Must contain at least one uppercase letter [A-Z].")
    if not re.search(r"[a-z]", password):
        failed_criteria.append("Must contain at least one lowercase letter [a-z].")
    if not re.search(r"\d", password):
        failed_criteria.append("Must contain at least one numerical digit [0-9].")
    if not re.search(r"[@$!%*?&]", password):
        failed_criteria.append("Must contain at least one special character [@$!%*?&].")
        
    return failed_criteria
'''

SAYS_SORT = r'''
def merge_sort(arr: list[int]) -> list[int]:
    """
    Sorts a list using the Divide-and-Conquer Merge Sort algorithm.
    Time Complexity: O(n log n) stable across all cases.
    Space Complexity: O(n) auxiliary due to sub-array generation.
    """
    # Base case: an array of 0 or 1 elements is already sorted
    if len(arr) <= 1:
        return arr

    # 1. Divide phase: Locate the median index point
    mid = len(arr) // 2
    
    # Recursively split and sort both left and right segments
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # 2. Conquer/Merge phase: Recombine the sorted sub-arrays
    return _merge(left_half, right_half)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Helper routine to merge two sorted arrays into a unified sorted array."""
    sorted_result = []
    i = j = 0

    # Compare elements from both arrays sequentially and append the smaller value
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sorted_result.append(left[i])
            i += 1
        else:
            sorted_result.append(right[j])
            j += 1

    # Append any remaining elements left over from either list slice
    sorted_result.extend(left[i:])
    sorted_result.extend(right[j:])
    
    return sorted_result
'''

SAYS_TREE = r'''
class Node:
    """Represents a single node within the Binary Search Tree."""
    
    def __init__(self, value: int) -> None:
        self.value: int = value
        self.left: Node | None = None
        self.right: Node | None = None


class BinarySearchTree:
    """Encapsulates the operational logic for a Binary Search Tree."""

    def __init__(self) -> None:
        self.root: Node | None = None

    def insert(self, value: int) -> None:
        """Public interface to insert a fresh value into the tree structure."""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current_node: Node, value: int) -> None:
        """Helper routine to traverse recursively and append nodes at leaf boundaries."""
        if value < current_node.value:
            if current_node.left is None:
                current_node.left = Node(value)
            else:
                self._insert_recursive(current_node.left, value)
        else:
            # Values greater than or equal to current go right
            if current_node.right is None:
                current_node.right = Node(value)
            else:
                self._insert_recursive(current_node.right, value)

    def search(self, target: int) -> bool:
        """Public lookup utility returning True if a value exists within the tree."""
        return self._search_recursive(self.root, target)

    def _search_recursive(self, current_node: Node | None, target: int) -> bool:
        """Helper routine utilizing BST properties to isolate targets in O(log n) average time."""
        if current_node is None:
            return False
        
        if current_node.value == target:
            return True
            
        if target < current_node.value:
            return self._search_recursive(current_node.left, target)
        
        return self._search_recursive(current_node.right, target)

    def get_inorder_list(self) -> list[int]:
        """
        Public interface executing an In-Order Traversal (Left, Root, Right).
        This traversal always extracts data out of a BST in perfectly sorted order.
        """
        result: list[int] = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, current_node: Node | None, result: list[int]) -> None:
        """Helper routine managing the deep traversal order stack."""
        if current_node is not None:
            self._inorder_recursive(current_node.left, result)   # Visit Left Subtree
            result.append(current_node.value)                   # Visit Root Node
            self._inorder_recursive(current_node.right, result)
'''

MODEL_REGEX = r'''
import re

_EMAIL_RE = re.compile(
    r"(?!\.)(?!.*\.\.)[A-Za-z0-9._%+-]+(?<!\.)"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"
)

_TR_PHONE_RE = re.compile(
    r"(?:\+90\s?|0\s?)?"
    r"[2-58]\d{2}\s?"
    r"\d{3}\s?"
    r"\d{2}\s?"
    r"\d{2}"
)

_UPPER_RE = re.compile(r"[A-ZÇĞİÖŞÜ]")
_LOWER_RE = re.compile(r"[a-zçğıöşü]")
_DIGIT_RE = re.compile(r"\d")
_SPECIAL_RE = re.compile(r"[^A-Za-z0-9ÇĞİÖŞÜçğıöşü\s]")

MIN_PASSWORD_LENGTH = 8


def validate_email(email: str) -> bool:
    if not isinstance(email, str) or len(email) > 254:
        return False
    return _EMAIL_RE.fullmatch(email) is not None


def validate_turkish_phone(phone: str) -> bool:
    if not isinstance(phone, str):
        return False
    return _TR_PHONE_RE.fullmatch(phone.strip()) is not None


def assess_password_strength(password: str) -> list[str]:
    if not isinstance(password, str):
        password = ""
    missing = []
    if len(password) < MIN_PASSWORD_LENGTH:
        missing.append("length")
    if not _UPPER_RE.search(password):
        missing.append("uppercase")
    if not _LOWER_RE.search(password):
        missing.append("lowercase")
    if not _DIGIT_RE.search(password):
        missing.append("digit")
    if not _SPECIAL_RE.search(password):
        missing.append("special")
    return missing


if __name__ == "__main__":
    for e in ["ali.veli@example.com", "a..b@example.com", ".ali@example.com", "ali@example", "ali@ex-ample.com.tr"]:
        print(f"email {e!r}: {validate_email(e)}")

    for p in ["+90 532 123 45 67", "+905321234567", "0532 123 45 67", "05321234567", "532 123 45 67", "0212 555 12 34", "+90 132 123 45 67", "0532 123 4567 8"]:
        print(f"phone {p!r}: {validate_turkish_phone(p)}")

    for pw in ["abc", "Password1", "Passw0rd!", "ŞifreÇok1!", "12345678"]:
        print(f"password {pw!r}: {assess_password_strength(pw)}")
'''

MODEL_SORT = r'''
def merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
'''

MODEL_TREE = r'''
class Node:
    __slots__ = ("value", "left", "right")

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
            return
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
            else:
                return

    def search(self, target) -> bool:
        current = self.root
        while current is not None:
            if target == current.value:
                return True
            current = current.left if target < current.value else current.right
        return False

    def get_inorder_list(self) -> list:
        result = []
        stack = []
        current = self.root
        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.value)
            current = current.right
        return result


if __name__ == "__main__":
    bst = BinarySearchTree()
    for v in [50, 30, 70, 20, 40, 60, 80, 30]:
        bst.insert(v)
    print(bst.get_inorder_list())
    print(bst.search(60))
    print(bst.search(65))
'''


sys.setrecursionlimit(1000)  # the default; set explicitly so the output is reproducible


def load(code: str) -> dict:
    ns = {"__name__": "answer"}  # keeps `if __name__ == "__main__"` blocks from running
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(code, "<answer>", "exec"), ns)
    return ns


def safe(fn, *args):
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return fn(*args)
    except BaseException as exc:  # RecursionError included on purpose
        return type(exc).__name__


# ----------------------------------------------------------------------------- tests
def tests_regex(ns):
    email, phone, pw = ns["validate_email"], ns["validate_turkish_phone"], ns["assess_password_strength"]

    def missing(password):
        res = safe(pw, password)
        if isinstance(res, str):
            return res
        text = " ".join(res).lower()  # old code returns sentences, new code returns keys
        return [k for k in ("length", "uppercase", "lowercase", "digit", "special") if k in text]

    nbsp = " "
    return [
        ("email: normal address accepted", safe(email, "ahmet@gurmezin.com") is True, ""),
        ("email: trailing newline rejected", safe(email, "a@x.com\n") is False, safe(email, "a@x.com\n")),
        ("email: 'user@com' rejected", safe(email, "user@com") is False, ""),
        ("phone: normal formats accepted", safe(phone, "0555 123 45 67") is True and safe(phone, "+905551234567") is True, ""),
        ("phone: Arabic-Indic digits rejected", not safe(phone, "5٥٥١٢٣٤٥٦٧"), safe(phone, "5٥٥١٢٣٤٥٦٧")),
        ("phone: newlines between groups rejected", not safe(phone, "0555\n123\n45\n67"), safe(phone, "0555\n123\n45\n67")),
        ("phone: trailing newline rejected", not safe(phone, "5551234567\n"), safe(phone, "5551234567\n")),
        ("phone: no-break spaces rejected", not safe(phone, f"0555{nbsp}123{nbsp}45{nbsp}67"), safe(phone, f"0555{nbsp}123{nbsp}45{nbsp}67")),
        ("password: 'Şifre123!x' is strong", missing("Şifre123!x") == [], missing("Şifre123!x")),
        ("password: 'çğışöü12!A' is strong", missing("çğışöü12!A") == [], missing("çğışöü12!A")),
        ("password: 'ŞİFRE123!' lacks lowercase", missing("ŞİFRE123!") == ["lowercase"], missing("ŞİFRE123!")),
        ("password: 'şifre123!x' lacks uppercase", missing("şifre123!x") == ["uppercase"], missing("şifre123!x")),
    ]


@dataclass(order=True)
class Record:
    score: int
    name: str = field(compare=False)


def tests_sort(ns):
    sort = ns["merge_sort"]
    rng = random.Random(1)
    lists = [[rng.randint(-50, 50) for _ in range(rng.randint(0, 60))] for _ in range(1000)]
    records = [Record(1, "Ayse"), Record(0, "Can"), Record(1, "Berk"), Record(1, "Deniz")]
    result = safe(sort, records)
    names = " ".join(r.name for r in result) if isinstance(result, list) else result
    one, zero = [42], []
    r1, r0 = safe(sort, one), safe(sort, zero)
    big = list(range(20000, 0, -1))
    return [
        ("1000 random lists == sorted()", all(safe(sort, list(x)) == sorted(x) for x in lists), ""),
        ("equal keys keep their order (stable)", names == "Can Ayse Berk Deniz", names),
        ("one element: a new list comes back", isinstance(r1, list) and r1 is not one, "same object" if r1 is one else ""),
        ("zero elements: a new list comes back", isinstance(r0, list) and r0 is not zero, "same object" if r0 is zero else ""),
        ("20000 reversed elements", safe(sort, big) == sorted(big), ""),
    ]


def tests_tree(ns):
    cls = ns["BinarySearchTree"]

    def build(values):
        tree = cls()
        for v in values:
            tree.insert(v)
        return tree

    shuffled = list(range(1000))
    random.Random(1).shuffle(shuffled)
    tree = safe(build, shuffled)
    typical = not isinstance(tree, str) and tree.get_inorder_list() == sorted(shuffled) \
        and all(tree.search(v) for v in shuffled) and not tree.search(1000)
    rows = [("1000 shuffled inserts: search + in-order", typical, "")]
    for n in (900, 1000, 5000):
        tree = safe(build, range(n))
        ok = not isinstance(tree, str) and tree.search(n - 1) is True and tree.get_inorder_list() == list(range(n))
        rows.append((f"{n} sorted inserts without a crash", ok, tree if isinstance(tree, str) else ""))
    dup = safe(build, [5, 3, 5, 8, 3])
    inorder = dup if isinstance(dup, str) else dup.get_inorder_list()
    rows.append(("duplicates: in-order == sorted([5,3,5,8,3])", inorder == [3, 3, 5, 5, 8], inorder))

    def took(values):
        start = time.perf_counter()
        safe(build, values)
        return time.perf_counter() - start

    ordered, mixed = list(range(3000)), list(range(3000))
    random.Random(2).shuffle(mixed)
    t_sorted, t_mixed = took(ordered), took(mixed)
    rows.append(("3000 sorted inserts < 10x the shuffled time", t_sorted < 10 * max(t_mixed, 1e-4),
                 f"sorted {t_sorted * 1000:.0f} ms, shuffled {t_mixed * 1000:.0f} ms"))
    return rows


AREAS = {
    "regex": (tests_regex, SAYS_REGEX, MODEL_REGEX),
    "sort": (tests_sort, SAYS_SORT, MODEL_SORT),
    "tree": (tests_tree, SAYS_TREE, MODEL_TREE),
}


def show(area: str, says_code: str | None, model_code: str) -> None:
    tests = AREAS[area][0]
    model = tests(load(model_code))
    says = tests(load(says_code)) if says_code else None
    print(f"\n== {area} ==")
    print(f"  {'test':<48} {'says':<6} {'model':<6} detail (model)")
    for i, (label, ok, detail) in enumerate(model):
        s = "-" if says is None else ("pass" if says[i][1] else "FAIL")
        print(f"  {label:<48} {s:<6} {'pass' if ok else 'FAIL':<6} {detail if not ok else ''}")


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] in AREAS:
        with open(sys.argv[2], encoding="utf-8") as fh:
            show(sys.argv[1], None, fh.read())
        return
    for area, (_, says_code, model_code) in AREAS.items():
        show(area, says_code, model_code)


if __name__ == "__main__":
    main()
