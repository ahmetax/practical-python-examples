# Factorial Calculation Project

A concise Python project that implements a recursive function to calculate the factorial of a given number. This project demonstrates the concept of recursion in Python.

## 🚀 Quick Start (Create from Scratch)

Follow these simple steps to recreate this project on your machine:

### 1. Setup Folder
Create a dedicated directory for the project:
```bash
mkdir 03_factorial
cd 03_factorial
```

### 2. Create the Code
Create a file named `factorial.py` and paste the following implementation:

```python
"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

def factorial(i: int) -> int:
    if i == 0:
        return 1
    return i * factorial(i - 1)

# Calculate factorial of 15
print(factorial(15))
```

### 3. Run and Verify
Execute the script using Python:
```bash
python3 factorial.py
```

**Expected Output:**
`1307674368000`

---

## 📂 Project Structure
```text
03_factorial/
└── factorial.py    # Contains the recursive factorial logic and a test case
```

## 🛠️ Requirements
- **Python**: Version 3.12 is recommended.
- **OS**: Compatible with all major operating systems (developed on Ubuntu 24.04).

## 📖 Technical Explanation
This project uses **Recursion**, a technique where a function calls itself to solve a smaller instance of the same problem.

- **Base Case**: If the input `i` is 0, the function returns 1 (since $0! = 1$).
- **Recursive Step**: For any $i > 0$, the function returns $i \times \text{factorial}(i - 1)$.

**Mathematical Logic:**
$n! = n \times (n-1) \times (n-2) \times \dots \times 1$
