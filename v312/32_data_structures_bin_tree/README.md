# Project 32: Binary Search Tree

A binary search tree (BST) built from scratch with two classes, `Node` and `BinarySearchTree`. Values smaller than a node go to its left, values greater than or equal to it go to its right. The tree supports three operations:

| Method | What it does |
|--------|--------------|
| `insert(value)` | Walks down from the root and adds the value as a new leaf |
| `search(target)` | Returns `True` or `False`; at each node it continues only into the left or the right subtree |
| `get_inorder_list()` | In-order traversal (left, node, right), which returns the values in sorted order |

There is no delete or update operation.

## How It Works
- `Node` holds a `value` and two references, `left` and `right`, both starting as `None`.
- `insert()`, `search()` and the traversal are all recursive helper methods (`_insert_recursive`, `_search_recursive`, `_inorder_recursive`).
- Duplicates are allowed: an equal value goes to the right subtree, so inserting `5` three times gives `[5, 5, 5]` in the traversal.
- Search and insert take O(log n) steps on average, but only when the tree stays balanced. The tree does not balance itself: if you insert values that are already sorted, every node goes to the right, the tree becomes a linked list and both operations take O(n) steps. Because the methods are recursive, inserting 1,000 sorted values (`for i in range(1000): bst.insert(i)`) stops with `RecursionError: maximum recursion depth exceeded` under the default recursion limit.

## Project Structure
```text
32_data_structures_bin_tree/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.11 or newer. The `Node | None` annotations need 3.10, but `main.py` also contains `from typing import Self` (added in 3.11, not used in the code), so on Python 3.10 the script stops with `ImportError: cannot import name 'Self' from 'typing'`. Tested on 3.12.3 and 3.11.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Custom Binary Search Tree Engine Started ---

Inserting data sequentially: [50, 30, 70, 20, 40, 60, 80]
Tree populated successfully.
-------------------------------------------------------
=== 1. Tree Traversal Assessment ===
In-Order Traversal Output (Sorted): [20, 30, 40, 50, 60, 70, 80]
-------------------------------------------------------

=== 2. Targeted Binary Lookup Testing ===
Searching for target element [40]: FOUND
Searching for target element [99]: NOT FOUND
Searching for target element [20]: FOUND
-------------------------------------------------------
```
The insertion order `[50, 30, 70, 20, 40, 60, 80]` produces a perfectly balanced tree of depth 3.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/09/01/python-ile-ikili-arama-agaci-verileri-kendi-kendine-siralayan-bir-yapi-kurmak/
- Python Tutorial, Classes: https://docs.python.org/3/tutorial/classes.html
