# 🔢 Armstrong Number Checker

A simple and efficient Python program that identifies Armstrong numbers within a specified range.

## 🧐 What is an Armstrong Number?
An **Armstrong number** (also known as a narcissistic number) is a number that is equal to the sum of its own digits each raised to the power of the number of digits.

**Example:**
For the number $153$:
- Number of digits = $3$
- Calculation: $1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153$
- Since the sum equals the original number, $153$ is an Armstrong number.

**Example:**
For the number $9474$:
- Number of digits = $4$
- Calculation: $9^4 + 4^4 + 7^4 + 4^4 = 6561 + 256 + 2401 + 256 = 9474$
- Since the sum equals the original number, $9474$ is an Armstrong number.

---

## 📁 Project Structure
```text
02_armstrong_number/
└── check_armstrong_number.py  # Main logic and execution script
```

---

## 🛠️ Setup and Installation

### 1. Prerequisites
- **Python 3.12+** installed.
- This project uses standard Python libraries and requires no external dependencies.

### 2. Quick Start
1. Create a folder named `02_armstrong_number`.
2. Create a file inside it named `check_armstrong_number.py`.
3. Copy the code from the source file into this script.

---

## 🏃 Running the Program

Execute the script using the Python interpreter:

```bash
python check_armstrong_number.py
```

### What happens when you run it?
The program iterates through all integers from **0 to 99,999** and prints every number that satisfies the Armstrong condition to the console.

---

## 📖 Code Explanation

### `is_armstrong(n)` function
This function takes an integer `n` and returns a boolean (`True` or `False`).
1. **String Conversion**: It converts the number to a string to easily iterate through each digit.
2. **Digit Count**: It calculates the length of the string to determine the power ($n$) for each digit.
3. **Summation**: It iterates through each character, converts it back to an integer, raises it to the power of the total digits, and adds it to a running sum.
4. **Comparison**: Finally, it compares the total sum with the original number.

### `main()` function
- Sets the search range (currently `0` to `100,000`).
- Loops through the range and calls `is_armstrong()` for each number.
- Prints the number if it is identified as an Armstrong number.

---

## 🚀 Complexity Analysis
- **Time Complexity**: $O(R \cdot D)$, where $R$ is the range of numbers checked and $D$ is the number of digits in the largest number.
- **Space Complexity**: $O(D)$ to store the string representation of the number.
