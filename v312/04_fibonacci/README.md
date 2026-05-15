# Fibonacci Sequence Project

A Python project that implements the Fibonacci sequence using a recursive approach and tracks the execution time for each number in the sequence. This project demonstrates recursive function calls and basic performance measurement.

## 🚀 Quick Start (Create from Scratch)

Follow these simple steps to recreate this project on your machine:

### 1. Setup Folder
Create a dedicated directory for the project:
```bash
mkdir 04_fibonacci
cd 04_fibonacci
```

### 2. Create the Code
Create a file named `fibonacci.py` and paste the following implementation:

```python
"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

from time import perf_counter

def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def main():
    t0: int = perf_counter()
    t2 = t0
    for i in range(36):
        t1 = perf_counter()
        print(f"{i} : {fib(i)} ({(t1 - t2)*1000} ms)")
        t2 = t1

main()
```

### 3. Run and Verify
Execute the script using Python:
```bash
python3 fibonacci.py
```

**Expected Output:**
The script will print the index, the Fibonacci number, and the time taken to calculate it in milliseconds for numbers 0 through 35. You will notice the time increasing exponentially as the index grows.

---

## 📂 Project Structure
```text
04_fibonacci/
└── fibonacci.py    # Main script implementing the recursive Fibonacci logic and timing
```

## 🛠️ Requirements
- **Python**: Version 3.12 is recommended.
- **OS**: Compatible with all major operating systems (developed on Ubuntu 24.04).

## 📖 Technical Explanation

### Recursion
This project uses a **recursive** implementation of the Fibonacci sequence:
- **Base Case**: If $n < 2$, it returns $n$.
- **Recursive Step**: For $n \ge 2$, it returns the sum of the two preceding numbers: $fib(n-1) + fib(n-2)$.

### Performance Tracking
The script uses `time.perf_counter()` to measure the high-resolution time elapsed between calculations. 

**Observation**: Because this implementation uses naive recursion without memoization, the time complexity is exponential $O(2^n)$. This makes the performance drop significantly as $n$ increases, which is clearly visible in the script's output.
