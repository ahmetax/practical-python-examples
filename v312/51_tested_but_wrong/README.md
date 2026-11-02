# Project 51: Tested but Wrong — An Unstable Merge Sort and a Tree That Crashes at 997

Projects 31 (merge sort) and 32 (binary search tree) were written by an AI assistant. Their demo output is correct, and the tests an assistant would typically write for them pass: "the result equals `sorted(data)` for 1,000 random integer lists", "1,000 shuffled values can all be found". This script shows four problems those tests cannot see, and runs the same tests on corrected versions.

| | Original ("says") | Corrected ("checks") |
|---|---|---|
| Equal keys in `merge_sort` | reversed (`<` in the merge step) | original order kept (`<=`) |
| `merge_sort` on 0 or 1 elements | returns the caller's own list | returns a new list |
| Tree with sorted input | `RecursionError` after ~997 inserts | no crash (loops instead of recursion) |
| Lookup cost on sorted input | O(n) | still O(n): "O(log n)" needs a balanced tree |

## How It Works
- The original functions and classes from projects 31 and 32 are copied unchanged (type hints removed) as `says_merge_sort` and `SaysTree`.
- Section 1 runs the typical tests on both versions. All pass.
- Section 2 sorts records that compare by score only (`@dataclass(order=True)` with `field(compare=False)` for the name), once directly and once as a two-pass sort (by name, then by score).
- Section 3 sorts a one-element list and appends to the result.
- Section 4 inserts 900 and 1,000 sorted integers. The default recursion limit is 1,000; the crash point was 996–999 elements on Python 3.11–3.15, depending on the operation and how deep the call stack already is.
- Section 5 builds the iterative tree from 10,000 shuffled and 10,000 sorted integers and compares it with a plain list kept sorted by `bisect.insort`.

## Project Structure
```text
51_tested_but_wrong/
├── main.py
├── README.md
└── README_TR.md
```

## Requirements
- Python 3.9 or newer. Tested on 3.12.3 and in Docker on 3.9, 3.13 and 3.15.
- No third-party packages.

## Running
```bash
python3 main.py
```
Section 5 takes a few seconds (building the degenerate tree is O(n²)).

## Sample Output (Python 3.12.3)
```text
Python 3.12.3

== 1. The typical tests ==
  says merge_sort        1000 random int lists == sorted(): True
  checks merge_sort      1000 random int lists == sorted(): True
  says tree              1000 shuffled inserts, search + in-order: True
  checks tree            1000 shuffled inserts, search + in-order: True

== 2. merge sort and equal keys ==
  input                  Ayse Can Berk Deniz   (Ayse, Berk, Deniz share score 1)
  sorted()               Can Ayse Berk Deniz
  says                   Can Deniz Berk Ayse
  checks                 Can Ayse Berk Deniz
  score, then name       expected Ali Bora Cem Dila Eda
  says (two passes)      Bora Ali Eda Dila Cem
  checks (two passes)    Ali Bora Cem Dila Eda

== 3. merge sort and short lists ==
  says                   same object: True   original after append: [42, -1]
  checks                 same object: False  original after append: [42]

== 4. sorted input and the recursive tree ==
  says, 900 sorted       ok, height 900
  says, 1000 sorted      RecursionError after 997 inserts
  checks, 1000 sorted    ok, height 1000

== 5. 'O(log n)' needs a balanced tree ==
  checks, 10000 shuffled height    34  build   0.03 s  2000 lookups  0.006 s
  checks, 10000 sorted   height 10000  build   5.77 s  2000 lookups  1.541 s
  bisect list, 10000 sorted               build   0.01 s  2000 lookups  0.002 s
```
Timings depend on the machine. On 3.9 and 3.13 the crash in section 4 comes after 996 inserts instead of 997; everything else is identical.

## Resources
- Blog post (Turkish): https://gurmezin.com/2026/11/16/testten-gecen-ama-yanlis-kararsiz-merge-sort-ikili-arama-agaci/
- Sort stability: https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts
- sys.setrecursionlimit: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
- bisect: https://docs.python.org/3/library/bisect.html
