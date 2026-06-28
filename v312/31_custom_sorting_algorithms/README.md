# Project 31: Custom Sorting Algorithms

A theoretical implementation analyzing array ordering mechanics by building classical sorting algorithms from scratch. This project features Bubble Sort to demonstrate nested-loop array traversal and Merge Sort to illustrate recursive divide-and-conquer strategies.

## Architectural Goal
The project bypasses Python's internal, highly optimized C-based `Timsort` (`.sort()`) engine to show how memory addresses, pointers, and array indices are shifted programmatically. It serves as a benchmark for comparing quadratic time execution ($O(n^2)$) with linearithmic time execution ($O(n \log n)$).

## Project Structure
```text
31_custom_sorting_algorithms/
└── main.py

System Requirements
OS: Ubuntu 24.04 (or any Linux/UNIX environment)

Runtime: Python 3.12+

Dependencies: None (Uses standard library built-ins)

How to Recreate This Project From Scratch
### Step 1: Directory Setup
Set up an isolated directory for this project inside your repository workspace:

```bash
mkdir 31_custom_sorting_algorithms
cd 31_custom_sorting_algorithms

### Step 2: Implement the Sorting Algorithms
Create a file named main.py. Build your sorting routines step-by-step:

Implement Bubble Sort: Write a function bubble_sort(arr). Create a shallow copy of the input list via list(arr) to keep the sorting operation pure and prevent unintended mutation of the original array reference. Use nested loops to compare adjacent elements and swap them if they are out of order. Add an optimization flag (swapped = False) to break out of the loop early if a pass completes without any changes, saving runtime on already sorted inputs.

Implement Merge Sort: Write a recursive function merge_sort(arr). Establish a base case that returns the collection immediately if its length is 1 or less. For larger lists, find the midpoint using floor division (//) and split the array into two halves (arr[:mid] and arr[mid:]). Pass those slices back into merge_sort recursively.

Build the Merge Combiner Utility: Create a private helper function _merge(left, right). Use two index pointer variables initialized to zero (i = j = 0) to step through both sorted lists simultaneously. Compare elements at the current pointers, append the lower value to a new results array, and advance that pointer. Use .extend() to append any remaining elements once one of the lists is exhausted.

### Step 3: Run and Verify
Add an evaluation block at the bottom of the script using an unsorted list containing arbitrary numbers (including negative values, zeroes, and duplicate entries). Execute the file from the terminal to verify that both algorithms return perfectly sorted lists:

```bash
python main.py


