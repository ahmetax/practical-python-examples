# 📊 CSV Processing Project

A practical demonstration of reading, filtering, and analyzing CSV data using Python. This project showcases two distinct approaches: one using Python's **standard library** (`csv` module) and another using the popular **Pandas** library for more advanced data manipulation.

## 🚀 Features

- **Sample Data Generation**: Automatically creates a test dataset (sales data with columns: product, category, quantity, unit_price, total).
- **Standard Library Approach**: Uses Python's built-in `csv` module to read, filter, and write data without external dependencies.
- **Pandas Approach**: Demonstrates the power of DataFrames for group-based statistical analysis.
- **Core Operations**: Filtering rows by column values, computing column statistics (min, max, sum, average), and writing output to new CSV files.

---

## 📁 Project Structure

```text
07_csv_processing/
└── csv_processing.py    # Main script containing all logic
```

---

## 🛠️ Step-by-Step Implementation Guide

### 1. Prerequisites
Ensure you have Python 3.12+ installed. This project requires the following library:
```bash
pip install pandas
```

### 2. Creating the Sample Data
Begin by creating a helper function that generates a CSV file with test data.
- Define a function `create_sample_csv(path)` that takes a file path as input.
- Use Python's built-in `open()` function with write mode (`"w"`).
- Write a header line with column names: `product,category,quantity,unit_price,total`.
- Add multiple rows of sample sales data representing different product categories (Electronics, Furniture, Stationery).
- Close the file and confirm creation.

### 3. Approach 1: Using Python's `csv` Module
This approach uses only the standard library, making it lightweight and dependency-free.

#### Reading CSV
- Create a function `read_csv_rows(path)` that opens the file in read mode.
- Use `csv.DictReader(f)` to parse the file. This returns an iterable of dictionaries where keys are the column headers.
- Convert the reader to a list and close the file.
- Return the list of dictionaries.

#### Displaying Data
- Create a `print_rows(rows)` function that iterates through the list and prints each row in a formatted table-like output.
- Access values using dictionary keys (e.g., `row["product"]`).

#### Filtering Data
- Implement `filter_by_category(rows, category)` that takes the list of rows and a category string.
- Iterate through the rows and append only those where `row["category"]` matches the input category into a new list.
- Return the filtered list.

#### Computing Statistics
- Build a `compute_stats(rows, column)` function that accepts a list of rows and the name of a numeric column.
- Initialize variables for `min_val`, `max_val`, and `total`.
- Loop through each row, convert the column value to a float, and update the statistics.
- Calculate the average by dividing the total by the count.
- Print the results.

#### Writing to CSV
- Write a function `write_filtered_csv(rows, path)` that saves filtered data to a new file.
- Extract field names from the keys of the first dictionary in the list.
- Use `csv.DictWriter(f, fieldnames=fieldnames)` to write the header and rows.
- Ensure the file is properly closed after writing.

### 4. Approach 2: Using Pandas
Pandas provides a more concise way to handle data aggregation and statistics.

- Implement a function `pandas_group_stats(path)` that loads the CSV file using `pd.read_csv(path)`.
- Use `df.groupby("category")["total"].agg(['sum', 'mean', 'count'])` to group the data by category and compute aggregate statistics for the "total" column.
- Iterate through the resulting grouped object and print the statistics for each category.

### 5. The Main Execution Flow
- Define a `main()` function that orchestrates the entire process.
- Set the paths for the source CSV and the filtered output file.
- Call the sample CSV creation function.
- Call each function sequentially to demonstrate the workflow:
  1. Read the CSV.
  2. Print the data.
  3. Filter by a specific category (e.g., "Electronics").
  4. Compute statistics on the filtered data.
  5. Write the filtered results to a new file.
  6. Run the Pandas aggregation example to show group-based analysis.

---

## 🏃 How to Run

1. Ensure you have the dependencies installed:
   ```bash
   pip install pandas
   ```
2. Run the script:
   ```bash
   python csv_processing.py
   ```

---

## 📖 Key Concepts Demonstrated

- **File I/O**: Reading from and writing to CSV files.
- **Data Structures**: Using Python lists and dictionaries to represent tabular data.
- **Filtering**: Iterating through collections to select specific subsets.
- **Aggregation**: Manually computing statistical values.
- **Pandas DataFrame**: Understanding how Pandas simplifies data manipulation through its DataFrame abstraction.