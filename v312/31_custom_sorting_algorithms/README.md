# Project 31: Custom Sorting Algorithms

Two classic sorting algorithms written from scratch, without `sorted()` or `list.sort()`:

| Function | Algorithm | Time complexity |
|----------|-----------|-----------------|
| `bubble_sort()` | Repeatedly swaps neighbouring elements that are out of order | O(n²), O(n) on an already sorted list |
| `merge_sort()` | Splits the list in half recursively, then merges the sorted halves | O(n log n) |

Both functions return a new list and leave the input list unchanged.

## How It Works
- **Bubble sort:** Works on a copy (`list(arr)`). After each pass the largest remaining element has moved to the end, so the inner loop gets one step shorter. If a pass makes no swap, the list is already sorted and the loop stops early.
- **Merge sort:** A list with 0 or 1 elements is returned as is. Longer lists are split at `len(arr) // 2`, both halves are sorted recursively, and `_merge()` combines them by walking two indexes `i` and `j` through the halves and always taking the smaller element.
- The demo sorts the same list (with a negative number, a zero and a duplicate `22`) with both functions and prints the original list at the end to show it was not changed.
- This `merge_sort()` is **not stable**: `_merge()` uses `left[i] < right[j]`, so when two elements are equal the one from the right half is taken first. This makes no difference for plain integers, but records with equal keys can change order. `left[i] <= right[j]` would keep the original order.

## Project Structure
```text
31_custom_sorting_algorithms/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer (the `list[int]` annotations need 3.9). Tested on 3.12.3 and 3.10.
- No third-party packages.

## Running
```bash
python3 main.py
```

## Sample Output (Python 3.12.3)
```text
--- Custom Sorting Engine Initialized ---

Original Unsorted Array : [64, 34, 25, 12, 22, 11, 90, -5, 0, 22]
------------------------------------------------------------
=== 1. Executing Bubble Sort O(n^2) ===
Bubble Sorted Result    : [-5, 0, 11, 12, 22, 22, 25, 34, 64, 90]
------------------------------------------------------------

=== 2. Executing Merge Sort O(n log n) ===
Merge Sorted Result     : [-5, 0, 11, 12, 22, 22, 25, 34, 64, 90]
------------------------------------------------------------

Verification (Original remains safe): [64, 34, 25, 12, 22, 11, 90, -5, 0, 22]
```
The script does not measure time. On a test machine, sorting 3,000 random integers took about 1.5 s with `bubble_sort()` and about 0.02 s with `merge_sort()`; your figures will differ.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/08/28/python-ile-siralama-algoritmalari-bubble-sort-ve-merge-sort-karsilastirmasi/
- Python Sorting Techniques: https://docs.python.org/3/howto/sorting.html
