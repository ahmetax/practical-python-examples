# Author: Ahmet Aksoy & Claude
# Date: 02.11.2026
# Python 3.12 (3.12.3) Ubuntu 24.04 - runs on Python 3.9+ (checked on 3.9, 3.13, 3.15 in Docker)

"""
Algorithms that pass their tests and are still wrong.

Projects 31 (merge sort) and 32 (binary search tree) were written by an AI
assistant. Their demo inputs work and a typical test ("result == sorted(data)",
"random inserts can be found") passes. This script shows what those tests do
not see, then runs the same checks on corrected versions.

  says   = original code from projects 31 and 32 (copied unchanged)
  checks = corrected code

Sections:
  1. The typical tests: all pass for both versions
  2. merge sort is not stable (equal keys come out reversed)
  3. merge sort returns the caller's own list for 0 or 1 elements
  4. sorted input turns the tree into a chain: RecursionError near 1000
  5. iterative tree: no crash, but still O(n) per lookup on sorted input
"""

from __future__ import annotations

import bisect
import random
import sys
import time
from dataclasses import dataclass, field

sys.setrecursionlimit(1000)  # the default; set explicitly so the output is reproducible


# ---------------------------------------------------------------- project 31 (says)
def says_merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return _says_merge(says_merge_sort(arr[:mid]), says_merge_sort(arr[mid:]))


def _says_merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# -------------------------------------------------------------- merge sort (checks)
def checks_merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)  # always a new list, like sorted()
    mid = len(arr) // 2
    return _checks_merge(checks_merge_sort(arr[:mid]), checks_merge_sort(arr[mid:]))


def _checks_merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # on a tie take the left one: this keeps the sort stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------- project 32 (says)
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class SaysTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, target):
        return self._search_recursive(self.root, target)

    def _search_recursive(self, node, target):
        if node is None:
            return False
        if node.value == target:
            return True
        if target < node.value:
            return self._search_recursive(node.left, target)
        return self._search_recursive(node.right, target)

    def get_inorder_list(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)


# -------------------------------------------------------------------- tree (checks)
class ChecksTree:
    """Same tree, same rules, but loops instead of recursion."""

    def __init__(self):
        self.root = None

    def insert(self, value):
        new = Node(value)
        if self.root is None:
            self.root = new
            return
        node = self.root
        while True:
            if value < node.value:
                if node.left is None:
                    node.left = new
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = new
                    return
                node = node.right

    def search(self, target):
        node = self.root
        while node is not None:
            if target == node.value:
                return True
            node = node.left if target < node.value else node.right
        return False

    def get_inorder_list(self):
        result, stack, node = [], [], self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.value)
            node = node.right
        return result


def height(root):
    best, stack = 0, [(root, 1)]
    while stack:
        node, depth = stack.pop()
        if node is not None:
            best = max(best, depth)
            stack.append((node.left, depth + 1))
            stack.append((node.right, depth + 1))
    return best


@dataclass(order=True)
class Record:
    score: int
    name: str = field(compare=False)  # compared by score only, like sort(key=...)


def names(records):
    return " ".join(r.name for r in records)


def row(label, text):
    print(f"  {label:<22} {text}")


# -------------------------------------------------------------------------- sections
def section_typical_tests():
    print("\n== 1. The typical tests ==")
    rng = random.Random(1)
    lists = [[rng.randint(-50, 50) for _ in range(rng.randint(0, 60))] for _ in range(1000)]
    for label, sort in (("says", says_merge_sort), ("checks", checks_merge_sort)):
        ok = all(sort(data) == sorted(data) for data in lists)
        row(f"{label} merge_sort", f"1000 random int lists == sorted(): {ok}")

    values = list(range(1000))
    rng.shuffle(values)
    for label, cls in (("says", SaysTree), ("checks", ChecksTree)):
        tree = cls()
        for v in values:
            tree.insert(v)
        ok = all(tree.search(v) for v in values) and not tree.search(1000)
        ok = ok and tree.get_inorder_list() == sorted(values)
        row(f"{label} tree", f"1000 shuffled inserts, search + in-order: {ok}")


def section_stability():
    print("\n== 2. merge sort and equal keys ==")
    records = [Record(1, "Ayse"), Record(0, "Can"), Record(1, "Berk"), Record(1, "Deniz")]
    row("input", names(records) + "   (Ayse, Berk, Deniz share score 1)")
    row("sorted()", names(sorted(records)))
    row("says", names(says_merge_sort(records)))
    row("checks", names(checks_merge_sort(records)))

    # Two-pass sort: by name first, then by score. Only works if the second pass is stable.
    people = [Record(s, n) for n, s in (("Eda", 2), ("Ali", 1), ("Cem", 2), ("Bora", 1), ("Dila", 2))]
    by_name = sorted(people, key=lambda r: r.name)
    row("score, then name", "expected " + names(sorted(people, key=lambda r: (r.score, r.name))))
    row("says (two passes)", names(says_merge_sort(by_name)))
    row("checks (two passes)", names(checks_merge_sort(by_name)))


def section_aliasing():
    print("\n== 3. merge sort and short lists ==")
    for label, sort in (("says", says_merge_sort), ("checks", checks_merge_sort)):
        original = [42]
        result = sort(original)
        result.append(-1)
        row(label, f"same object: {result is original!s:<5}  original after append: {original}")


def section_recursion():
    print("\n== 4. sorted input and the recursive tree ==")
    for n in (900, 1000):
        tree = SaysTree()
        try:
            for v in range(n):
                tree.insert(v)
            row(f"says, {n} sorted", f"ok, height {height(tree.root)}")
        except RecursionError:
            row(f"says, {n} sorted", f"RecursionError after {count(tree.root)} inserts")
    tree = ChecksTree()
    for v in range(1000):
        tree.insert(v)
    row("checks, 1000 sorted", f"ok, height {height(tree.root)}")


def count(root):
    total, stack = 0, [root]
    while stack:
        node = stack.pop()
        if node is not None:
            total += 1
            stack.extend((node.left, node.right))
    return total


def timed(fn):
    start = time.perf_counter()
    fn()
    return time.perf_counter() - start


def section_complexity():
    print("\n== 5. 'O(log n)' needs a balanced tree ==")
    n = 10000
    shuffled = list(range(n))
    random.Random(2).shuffle(shuffled)
    for label, data in (("shuffled", shuffled), ("sorted", list(range(n)))):
        tree = ChecksTree()
        build = timed(lambda: [tree.insert(v) for v in data])
        look = timed(lambda: [tree.search(v) for v in range(0, n, 5)])
        row(f"checks, {n} {label}", f"height {height(tree.root):>5}  build {build:6.2f} s  2000 lookups {look:6.3f} s")

    items = []
    build = timed(lambda: [bisect.insort(items, v) for v in range(n)])
    look = timed(lambda: [_bisect_has(items, v) for v in range(0, n, 5)])
    row(f"bisect list, {n} sorted", f"              build {build:6.2f} s  2000 lookups {look:6.3f} s")


def _bisect_has(items, value):
    i = bisect.bisect_left(items, value)
    return i < len(items) and items[i] == value


if __name__ == "__main__":
    print("Python", sys.version.split()[0])
    section_typical_tests()
    section_stability()
    section_aliasing()
    section_recursion()
    section_complexity()
