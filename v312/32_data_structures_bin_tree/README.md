# Project 32: Binary Search Tree Data Structure

An object-oriented implementation of a standalone Binary Search Tree (BST) built natively from scratch. This project demonstrates reference/pointer node linkage, conditional traversal mechanics, and deep recursive tree manipulation strategies.

## Architectural Goal
The application provides a structural alternative to flat indexing tables. By maintaining hierarchical branch properties—where any child entity left of a parent holds a lesser evaluation, and any child right holds a greater value—the system establishes execution frameworks capable of running lookups and node updates in linearithmic logarithmic time ($O(\log n)$).

## Project Structure
```text
32_data_structures_bin_tree/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX-compatible ecosystem)
Runtime: Python 3.12+ (Leverages modern union notation Node | None)
Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Create a dedicated project directory structure within your repository workspace:
```bash
mkdir 32_data_structures_bin_tree
cd 32_data_structures_bin_tree

### Step 2: Assemble the Tree Classes
Create a file named main.py. Structure your hierarchical entities step-by-step:
1. Design a Node Blueprint: Create a basic structure class called Node. Inside its initializer (__init__), accept an integer data variable, and map two default child pointer fields initialized explicitly to None (self.left and self.right).
2. Design the Master Tree Shell: Create a coordinating class called BinarySearchTree initialized with an empty single entry pointer (self.root = None).
3. Incorporate Recursive Insertion: Create a public insert(value) method. If self.root doesn't exist, bind the new value there immediately. Otherwise, pass the node down to an internal tracking method _insert_recursive(current_node, value). Compare the new value to the current node value to determine whether to branch left or right, and recursively follow the tree until a vacant leaf position (None) is found.
4. Incorporate Specialized Lookup Routing: Implement a search(target) function that steps down branches recursively. Since the data is organized, you don't need to scan every node; lookups can jump past entire sub-trees based on value comparisons, achieving an average time complexity of $O(\log n)$.
5. Implement an In-Order Sort Traversal: Build an analytical visualization sequence using an in-order algorithm strategy (_inorder_recursive(node, list)). Program the traversal sequence order to step left first, collect the parent center second, and traverse right last. When performed on a valid BST layout, this strategy naturally outputs values in perfectly sorted ascending order.

### Step 3: Run and Verify
Add a driver evaluation script at the bottom of main.py. Instantiate your class, populate it with an unsorted array of numbers, execute an in-order print lookup, and attempt targeted value queries to verify your tracking logic. Run the script:

```bash
python main.py
