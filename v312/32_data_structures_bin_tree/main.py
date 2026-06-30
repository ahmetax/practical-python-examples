# Author: Ahmet Aksoy
# Date: 23.05.2026
# Python3.12 Ubuntu 24.04

"""
Binary Search Tree (BST) Data Structure Example
Demonstrates object-oriented data structures, pointer/reference management,
and recursive traversal algorithms (In-order) from scratch.
"""

from typing import Self


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
            self._inorder_recursive(current_node.right, result)  # Visit Right Subtree


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Custom Binary Search Tree Engine Started ---\n")

    bst = BinarySearchTree()
    
    # Dataset to insert (mixed order)
    dataset = [50, 30, 70, 20, 40, 60, 80]
    print(f"Inserting data sequentially: {dataset}")
    
    for item in dataset:
        bst.insert(item)
    print("Tree populated successfully.")
    print("-" * 55)

    print("=== 1. Tree Traversal Assessment ===")
    # An in-order traversal across a true BST must yield a sorted list
    sorted_output = bst.get_inorder_list()
    print(f"In-Order Traversal Output (Sorted): {sorted_output}")
    print("-" * 55)

    print("\n=== 2. Targeted Binary Lookup Testing ===")
    search_targets = [40, 99, 20]
    
    for target in search_targets:
        found = bst.search(target)
        status_text = "FOUND" if found else "NOT FOUND"
        print(f"Searching for target element [{target}]: {status_text}")
    print("-" * 55)