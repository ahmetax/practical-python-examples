# 🔢 Prime Numbers Generator

A simple and efficient Python program that finds and prints all prime numbers within a specified range.

## 🧐 What is a Prime Number?
A **prime number** is a natural number greater than 1 that has no positive divisors other than 1 and itself.

**Examples:**
- **2**: The only even prime number.
- **3**: Prime, as it is only divisible by 1 and 3.
- **5**: Prime, as it is only divisible by 1 and 5.
- **4**: Not prime, as it is divisible by 1, 2, and 4.

---

## 📁 Project Structure
```text
05_prime_numbers/
└── prime_numbers.py  # Main logic and execution script
```

---

## 🛠️ Setup and Installation

### 1. Prerequisites
- **Python 3.12+** installed.
- This project uses standard Python libraries and requires no external dependencies.

### 2. Quick Start
1. Create a folder named `05_prime_numbers`.
2. Create a file inside it named `prime_numbers.py`.
3. Copy the code from the source file into this script.

---

## 🏃 Running the Program

Execute the script using the Python interpreter:

```bash
python prime_numbers.py
```

### What happens when you run it?
The program iterates through all integers from **0 up to 127** and prints every prime number found to the console.

---

## 📖 Code Explanation

### Logic Breakdown
The program uses a technique called **Trial Division** to identify primes:

1. **Range Definition**: It defines a `lownum` (start) and `highnum` (end).
2. **Outer Loop**: It iterates through every number `n` in the range `[lownum, highnum]`.
3. **Prime Filtering**:
    - It skips numbers less than or equal to 1, as they are not prime by definition.
    - For each number `n > 1`, it starts another loop iterating from `2` up to `n-1`.
4. **Divisibility Check**: If `n` is divisible by any number `i` in that range (`n % i == 0`), the number is not prime, and the inner loop is broken.
5. **The `for...else` Block**: Python's unique `else` clause attached to a `for` loop executes **only if the loop completes normally** (i.e., it never hit the `break` statement). If no divisors were found, the number is prime and is printed.

---

## 🚀 Complexity Analysis
- **Time Complexity**: $O(N^2)$ in the worst case, where $N$ is the `highnum`, because for every number, it potentially checks all preceding numbers.
- **Space Complexity**: $O(1)$, as it only uses a few variables regardless of the range size.
