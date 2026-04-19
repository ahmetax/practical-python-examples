"""
Author: Ahmet Aksoy
Date: 2026-04-19
Python 3.12 - Ubuntu 24.04

Description:
    Reading and processing CSV files.

    Two approaches are demonstrated:
      1. Standard library  — Python's built-in csv module, no dependencies
      2. Pandas            — for more complex data operations

    In both cases, PythonObject is used explicitly in function signatures,
    making it clear which variables hold Python values vs Mojo values.

    The example uses a small sales dataset that is generated at runtime,
    so no external CSV file is needed.

    Operations covered:
      - Reading a CSV file row by row
      - Filtering rows by a condition
      - Computing column statistics (min, max, average)
      - Writing a filtered result to a new CSV file
      - Reading the same data with Pandas and computing group statistics

Requirements:
    pip install pandas
"""

# ------------------------------------------------------------
# Helper: create a sample CSV file for testing
# ------------------------------------------------------------

def create_sample_csv(path) -> None:
    """
    Writes a small sales dataset to a CSV file.
    Columns: product, category, quantity, unit_price, total.
    """

    f = open(path, "w")
    f.write("product,category,quantity,unit_price,total\n")
    f.write("Keyboard,Electronics,10,450.00,4500.00\n")
    f.write("Mouse,Electronics,25,150.00,3750.00\n")
    f.write("Desk,Furniture,5,1200.00,6000.00\n")
    f.write("Chair,Furniture,8,950.00,7600.00\n")
    f.write("Monitor,Electronics,12,3200.00,38400.00\n")
    f.write("Notebook,Stationery,100,15.00,1500.00\n")
    f.write("Pen,Stationery,500,3.50,1750.00\n")
    f.write("Headphones,Electronics,7,800.00,5600.00\n")
    f.write("Lamp,Furniture,15,320.00,4800.00\n")
    f.write("USB Hub,Electronics,20,250.00,5000.00\n")
    f.close()
    print("Sample CSV created:", path)


# ------------------------------------------------------------
# Pattern 1: Reading CSV with Python's csv module
# ------------------------------------------------------------
import csv
import pandas as pd

def read_csv_rows(path):
    """
    Reads a CSV file using the csv.DictReader.
    Returns a Python list of dicts, one dict per row.
    Each dict key is the column name, value is the cell string.

    DictReader is preferred over reader() because it gives
    named access to columns instead of positional index.
    """

    f = open(path, "r", newline="")
    reader = csv.DictReader(f)

    # Collect all rows into a Python list
    rows = list(reader)
    f.close()

    print("Read", len(rows), "rows from", path)
    return rows


def print_rows(rows):
    """Print all rows in a simple tabular format."""
    count = len(rows)
    print()
    print("  Product          Category       Qty   Unit Price      Total")
    print("  " + "-" * 64)
    for i in range(count):
        row = rows[i]
        print(" ",
            row["product"] + "            ",
            row["category"] + "        ",
            row["quantity"],
            row["unit_price"],
            row["total"]
        )


def filter_by_category(rows, category):
    """
    Filter rows where the 'category' column matches the given value.
    Returns a new Python list with matching rows only.
    Demonstrates passing PythonObject between fn functions.
    """
    result = list()
    count = len(rows)

    for i in range(count):
        row = rows[i]
        if row["category"] == category:
            result.append(row)

    return result


def compute_stats(rows, column):
    """
    Compute min, max, and average for a numeric column.
    Values are read as PythonObject strings, converted to Mojo Float64
    for arithmetic, then printed.
    """
    count = len(rows)
    if count == 0:
        print("No rows to compute stats.")
        return

    total = 0.0
    min_val = float(rows[0][column])
    max_val = min_val

    for i in range(count):
        row = rows[i]
        val = float(row[column])
        total += val
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val

    avg = total / count
    print("  Column   :", column)
    print("  Count    :", count)
    print("  Min      :", min_val)
    print("  Max      :", max_val)
    print("  Average  :", avg)
    print("  Total    :", total)


def write_filtered_csv(rows, path):
    """
    Write a filtered set of rows to a new CSV file.
    Uses Python's csv.DictWriter to preserve column headers.
    """

    if len(rows) == 0:
        print("No rows to write.")
        return

    # Get column names from the first row's keys
    fieldnames = list(rows[0].keys())

    f = open(path, "w", newline="")
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    f.close()

    print("Wrote", len(rows), "rows to", path)


# ------------------------------------------------------------
# Pattern 2: Reading and grouping with Pandas
# ------------------------------------------------------------

def pandas_group_stats(path):
    """
    Read the CSV with Pandas and compute total sales per category.
    Demonstrates using PythonObject to work with a DataFrame.

    Pandas is more concise for aggregation tasks compared to
    manual iteration with the csv module.
    """

    # Read CSV into a DataFrame — all columns auto-detected
    df = pd.read_csv(path)

    print("DataFrame shape: rows =", df.shape[0], ", cols =", df.shape[1])
    print()

    # Group by category, sum the numeric columns
    grouped = df.groupby("category")["total"].agg(
        eval("['sum', 'mean', 'count']")
    )

    print("Sales summary by category:")
    print("  " + "-" * 44)

    # Iterate over grouped result rows
    categories= grouped.index.tolist()
    n = len(categories)

    for i in range(n):
        cat  = categories[i]
        row = grouped.loc[categories[i]]
        total = row["sum"]
        mean  = row["mean"]
        cnt = row["count"]
        print("  Category :", cat)
        print("    Count  :", cnt)
        print("    Total  :", total)
        print("    Average:", mean)
        print()


def main():
    csv_path      = "/tmp/sales.csv"
    filtered_path = "/tmp/sales_electronics.csv"

    # --- Setup ---
    print("=== Creating sample CSV ===")
    print()
    create_sample_csv(csv_path)

    # --- Pattern 1: csv module ---
    print()
    print("=== Reading CSV with csv module ===")
    rows = read_csv_rows(csv_path)
    print_rows(rows)

    print()
    print("=== Filtering: Electronics only ===")
    electronics = filter_by_category(rows, "Electronics")
    print_rows(electronics)

    print()
    print("=== Stats for 'total' column (Electronics) ===")
    compute_stats(electronics, "total")

    print()
    print("=== Writing filtered CSV ===")
    write_filtered_csv(electronics, filtered_path)

    # --- Pattern 2: Pandas ---
    print()
    print("=== Group statistics with Pandas ===")
    print()
    pandas_group_stats(csv_path)

main()