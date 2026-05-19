# 📂 File and Word Counter

A simple Python utility that recursively traverses a directory, finds all `.txt` files, and counts the total number of files and words within them. It demonstrates the use of Python's `pathlib` library for file system operations and recursion for directory traversal.

## 🚀 Features

- **Recursive Directory Traversal**: Scans all subdirectories within a given root path.
- **File Filtering**: Only processes files with the `.txt` extension.
- **Word Counting**: Reads each text file and counts the total number of words.
- **Progress Output**: Prints the word count for each individual file as it is processed.
- **Summary Report**: Displays the total number of files and total word count at the end.

---

## 📁 Project Structure

```text
09_file_apps/
└── file_and_word_counter_01.py    # Main script containing all logic
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
- **Python 3.12+** installed.
- This project uses only Python's standard library (`pathlib`), so no external dependencies are required.

### 2. Creating the Script

#### Step 1: Import Required Modules
At the top of your script, import the `Path` class from the `pathlib` module:
```python
from pathlib import Path
```

#### Step 2: Create a Counter Class
Define a class to store the global counters:
- Create a class named `FileCounter`.
- Initialize instance variables `count` (for files) and `total_words` (for words) in the `__init__` method.

#### Step 3: Create a Word Counting Function
Define a helper function to count words in a single file:
- Function name: `count_words_in_file(filepath)`.
- Open the file in read mode (`"r"`).
- Read the entire content using `f.read()`.
- Close the file.
- Split the content by whitespace using `content.split()` to get a list of words.
- Return the length of the word list.

#### Step 4: Create the Recursive Processing Function
Define the main processing function:
- Function name: `process_txt_files(path, counter)`.
- **Step A — List Entries**: Use `path.glob("*")` to get all entries in the directory. Filter to keep only files (not directories).
- **Step B — Iterate**: Loop through each entry.
- **Step C — Recursion**: If the entry is a directory, recursively call `process_txt_files` on that subdirectory.
- **Step D — File Check**: If the entry is a file, check if its suffix (extension) is `.txt`.
- **Step E — Counting**:
  - Increment `counter.count`.
  - Call the word counting function to get the word count for this file.
  - Add the result to `counter.total_words`.
  - Print the progress: file number, file path, and word count.

#### Step 5: Create the Main Function
Define the entry point:
- Function name: `main()`.
- Instantiate a `FileCounter()` object.
- Define the target `Path` to scan (e.g., a folder path like `/path/to/your/folder`).
- **Validation**: Check if the path exists using `path.exists()`. If not, print an error message and return.
- Call `process_txt_files(path, counter)`.
- After processing, print a summary block showing the total number of files and total words.

#### Step 6: Execute Main
At the bottom of the script, call `main()` to start the program:
```python
main()
```

---

## 🏃 How to Run

1. Ensure you have a directory containing `.txt` files that you want to analyze (or use any existing folder).
2. Run the script:
   ```bash
   python file_and_word_counter_01.py
   ```

---

## 📖 Example Output

When you run the script, you will see output similar to:
```text
1 - /path/to/folder/file1.txt -> 1250 words
2 - /path/to/folder/subdir/file2.txt -> 340 words
3 - /path/to/folder/subdir/file3.txt -> 89 words

=== RESULTS ===
Total number of files:  3
Total number of words:  1679
```

---

## 🔧 Customization Tips

- **Change Target Folder**: Modify the `path` variable in the `main()` function to point to the folder you want to scan.
- **Different Extensions**: If you want to count other file types, change the condition `entry_name.suffix == ".txt"` to match your desired extension (e.g., `.md`, `.csv`).
- **Case Sensitivity**: The current suffix check is case-sensitive. To make it case-insensitive, use `entry_name.suffix.lower() == ".txt"`.

---

## 📚 Key Concepts Demonstrated

- **Object-Oriented Programming (OOP)**: Using a class to maintain state across recursive calls.
- **Recursion**: The function calls itself to handle nested directories.
- **File I/O**: Reading text files and handling paths safely using `pathlib`.
- **String Manipulation**: Using `.split()` to tokenize text into words.