# Author: Ahmet Aksoy
# Date: 22.05.2026
# Python3.12 Ubuntu 24.04

"""
Custom Sorting Algorithms Example
Demonstrates algorithmic complexity and step-by-step array manipulation 
by implementing Bubble Sort O(n^2) and Merge Sort O(n log n) from scratch.
"""


def bubble_sort(arr: list[int]) -> list[int]:
    """
    Sorts a mutable list in place using the Bubble Sort algorithm.
    Time Complexity: O(n^2) average/worst case.
    Space Complexity: O(1) auxiliary (In-place execution).
    """
    # Create a copy to prevent mutation of the original reference array
    data = list(arr)
    n = len(data)

    for i in range(n):
        # Optimization flag: if no elements swap during a pass, the list is sorted
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                # Swap neighboring elements
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
                
        # Break early if the collection is already ordered
        if not swapped:
            break
            
    return data


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


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Custom Sorting Engine Initialized ---\n")

    unsorted_dataset = [64, 34, 25, 12, 22, 11, 90, -5, 0, 22]
    print(f"Original Unsorted Array : {unsorted_dataset}")
    print("-" * 60)

    print("=== 1. Executing Bubble Sort O(n^2) ===")
    bubble_output = bubble_sort(unsorted_dataset)
    print(f"Bubble Sorted Result    : {bubble_output}")
    print("-" * 60)

    print("\n=== 2. Executing Merge Sort O(n log n) ===")
    merge_output = merge_sort(unsorted_dataset)
    print(f"Merge Sorted Result     : {merge_output}")
    print("-" * 60)
    
    # Confirming the original unsorted list was not mutated
    print(f"\nVerification (Original remains safe): {unsorted_dataset}")