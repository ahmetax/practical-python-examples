# λ Lambda Functions in Python

A comprehensive collection of examples demonstrating the use of **lambda functions** (anonymous functions) in Python. Lambda functions are small, inline functions defined using the `lambda` keyword without a formal `def` statement. They are particularly useful for short-lived operations, especially when used with built-in functions like `map()`, `filter()`, `sorted()`, and `reduce()`.

---

## 📁 Project Structure

```text
13_lambda_basics/
└── lambda_examples.py    # Main script with 20 lambda function examples
```

---

## 🛠️ Step-by-Step Implementation Guide

### Prerequisites
- Python 3.12+ installed
- No external dependencies required (uses only the standard library)

---

### Creating the Script

This project demonstrates 20 different use cases for lambda functions. Follow these steps to create each example from scratch.

---

### 1. Basic Setup

Create a new file named `lambda_examples.py` and start with the following imports:

```python
import operator
from functools import reduce
import math

def main():
    print("--- Python 3.12 Lambda Function Examples ---")
```

---

### 2. Example 1: Basic Addition

Create a lambda that takes two arguments and returns their sum.

**Logic**: Define `add` as a lambda function that accepts `x` and `y` and returns `x + y`. Call it with `add(5, 3)`.

---

### 3. Example 2: Squaring a Number

Create a lambda that takes one argument and returns its square.

**Logic**: Define `square` as `lambda x: x**2`. Call it with `square(4)`.

---

### 4. Example 3: Conditional (Ternary) Expression

Use a lambda with a ternary operator to check if a number is even or odd.

**Logic**: Define `check_even` as `lambda x: "Even" if x % 2 == 0 else "Odd"`. Call it with `check_even(7)`.

---

### 5. Example 4: Sorting a List of Tuples

Sort a list of tuples by the second element (the string) using a lambda as the key.

**Logic**: Create a list `pairs = [(1, 'one'), (2, 'two'), ...]`. Call `pairs.sort(key=lambda pair: pair[1])`.

---

### 6. Example 5: Filtering a List

Use `filter()` with a lambda to keep only even numbers from a list.

**Logic**: Create `nums = [1, 2, 3, 4, 5, 6]`. Apply `filter(lambda x: x % 2 == 0, nums)` and convert to a list.

---

### 7. Example 6: Mapping a Function to a List

Use `map()` with a lambda to double every number in a list.

**Logic**: Apply `map(lambda x: x * 2, nums)` and convert to a list.

---

### 8. Example 8: Currying (Lambda inside Lambda)

Create a "factory" function that returns another lambda — a classic currying pattern.

**Logic**: Define `multiplier = lambda x: lambda y: x * y`. Assign `double_func = multiplier(2)` and call `double_func(10)` to get 20.

---

### 9. Example 9: Sorting a Dictionary by Value

Sort a dictionary by its values in descending order using a lambda key.

**Logic**: Create `scores = {'Alice': 88, 'Bob': 95, 'Charlie': 80}`. Use `sorted(scores.items(), key=lambda item: item[1], reverse=True)`.

---

### 10. Example 10: Simple String Formatter

Use a lambda to format a greeting message.

**Logic**: Define `greet = lambda name: f"Hello, {name}! Welcome to Ubuntu 24.04."`. Call `greet('Developer')`.

---

### 11. Example 11: Extracting Data from List of Dictionaries

Use `map()` with a lambda to extract specific fields from a list of dictionaries.

**Logic**: Create `users = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]`. Extract names using `map(lambda u: u['name'], users)`.

---

### 12. Example 12: Summing with Reduce

Use `reduce()` from `functools` with a lambda to sum all elements in a list.

**Logic**: Import `reduce`. Apply `reduce(lambda x, y: x + y, [1, 2, 3, 4])`.

---

### 13. Example 13: Checking Palindrome

Use a lambda to check if a string reads the same forwards and backwards.

**Logic**: Define `is_palindrome = lambda s: s == s[::-1]`. Test with `'radar'`.

---

### 14. Example 14: Circle Area Calculation

Use a lambda with `math.pi` to calculate the area of a circle.

**Logic**: Define `circle_area = lambda r: math.pi * (r**2)`. Call with `r=5` and format to 2 decimal places.

---

### 15. Example 15: Celsius to Fahrenheit Conversion

Use a lambda to convert temperatures.

**Logic**: Define `c_to_f = lambda c: (c * 9/5) + 32`. Call with `c=25`.

---

### 16. Example 16: Filtering Strings by Prefix

Use `filter()` with a lambda to find strings that start with a specific letter.

**Logic**: Create `fruit_list = ["apple", "apricot", "banana", "cherry"]`. Filter with `lambda f: f.startswith('a')`.

---

### 17. Example 17: List Comprehension with Lambda

Use a lambda inside a list comprehension (though not the typical use case, it demonstrates lambda's versatility).

**Logic**: Create `[(lambda x: x**2)(x) for x in range(5)]` to generate a list of squares.

---

### 18. Example 18: Simple Logic Gate (AND)

Use a lambda to simulate a logical AND operation.

**Logic**: Define `logic_and = lambda a, b: a and b`. Test with `(True, False)`.

---

### 19. Example 19: Applying Operators Dynamically

Pass an operator function (from the `operator` module) as an argument to a lambda.

**Logic**: Define `apply_op = lambda op, x, y: op(x, y)`. Use `operator.mul` as the operator.

---

### 20. Example 20: Range Validation

Use a lambda to check if a number falls within a specified range.

**Logic**: Define `in_range = lambda x, start, end: start <= x <= end`. Test with `in_range(15, 10, 20)`.

---

### 3. Finishing the Script

After adding all examples, close the main function and call it:

```python
if __name__ == "__main__":
    main()
```

---

## 🏃 How to Run

1. Save the file as `lambda_examples.py`.
2. Run the script:
   ```bash
   python lambda_examples.py
   ```

---

## 📖 Output Example

When you run the script, you will see output similar to:

```text
--- Python 3.12 Lambda Function Examples ---
1. Addition (5+3): 8
2. Square (4): 16
3. Parity (7): Odd
4. Sorted tuples by name: [(1, 'one'), (3, 'three'), (4, 'four'), (2, 'two')]
5. Filtered evens: [2, 4, 6]
6. Mapped doubles: [2, 4, 6, 8, 10, 12]
7. Longest word: banana
8. Curried double (10): 20
9. Scores sorted desc: [('Bob', 95), ('Alice', 88), ('Charlie', 80)]
10. Greeting: Hello, Developer! Welcome to Ubuntu 24.04.
11. Extracted names: ['Alice', 'Bob']
12. Reduce sum: 10
13. Is 'radar' palindrome? True
14. Circle area (r=5): 78.54
15. 25C to F: 77.0
16. Fruits starting with 'a': ['apple', 'apricot']
17. List comprehension lambda squares: [0, 1, 4, 9, 16]
18. Logic AND (True, False): False
19. Using operator.mul via lambda: 50
20. Is 15 in range 10-20? True
```

---

## 🔑 Key Concepts Demonstrated

1. **Anonymous Functions**: Creating functions without a name using the `lambda` keyword.
2. **Single-Line Logic**: Writing concise functions for simple operations.
3. **Functional Programming**: Using lambda with `map()`, `filter()`, `sorted()`, `max()`, and `reduce()`.
4. **Higher-Order Functions**: Passing functions as arguments and returning functions (currying).
5. **Ternary Expressions**: Using conditional logic within lambdas.
6. **Data Transformation**: Extracting, filtering, and transforming lists and dictionaries.
7. **Mathematical Operations**: Performing calculations using lambdas.

---

## 💡 When to Use Lambdas

- **Short-lived operations**: When you need a function for a one-time use.
- **Functional programming**: When using `map`, `filter`, `reduce`, `sorted`, etc.
- **Callbacks**: When passing a small function as an argument to another function.
- **GUI event handling**: For simple event callbacks (e.g., in Tkinter).

---

## ⚠️ When NOT to Use Lambdas

- **Complex logic**: If the function requires multiple lines, use `def`.
- **Reusability**: If you need to call the function from multiple places, define it with `def`.
- **Debugging**: Lambdas are harder to debug since they lack a name.

---

## 🔧 Extension Ideas

- Write your own lambda expressions for common tasks.
- Use lambdas with `pandas` for DataFrame operations.
- Create a lambda-based utility module for your projects.
- Explore list comprehensions as an alternative to `map()` and `filter()`.