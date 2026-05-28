# Author: Ahmet Aksoy
# Date: 21.05.2026
# Python3.12 Ubuntu 24.04

"""
Python 3.10+ Structural Pattern Matching (match-case) Example
This example demonstrates how to use modern pattern matching techniques
instead of complex if-elif-else blocks for structural data validation.
"""

from dataclasses import dataclass


@dataclass
class Order:
    product_name: str
    quantity: int
    status: str  # "pending", "shipped", "delivered"


def process_command(command):
    """
    Analyzes different data structures (string, list, object, dict) 
    using structural pattern matching.
    """
    match command:
        # 1. Literal Matching (Exact Value)
        case "EXIT":
            print("Exiting system...")
            return False

        # 2. Sequence Matching (List length and type validation)
        # e.g., ["add", "Book", 3]
        case ["add", str(item), int(qty)]:
            print(f"Stock updated: Added {qty} units of '{item}'.")

        # 3. Rest of Sequence Matching with a Guard Condition
        # e.g., ["delete", 101, 102, 103]
        case ["delete", *id_list] if len(id_list) > 0:
            print(f"Deleting products with IDs: {id_list}")

        # 4. Object Matching (Dataclass inspection)
        # Matches only Order objects where status is "shipped"
        case Order(product_name=name, quantity=qty, status="shipped"):
            print(f"In-Transit: {name} ({qty} units) is currently with the carrier.")

        # Matches any other Order objects regardless of status
        case Order() as order:
            print(f"General Order Info: {order.product_name} - Status: {order.status}")

        # 5. Mapping Matching (Dictionary structure validation)
        case {"type": "invoice", "amount": float(amt)}:
            print(f"Invoice processed. Amount: ${amt:.2f}")

        # 6. Wildcard / Default Case (Catch-all)
        case _:
            print(f"Invalid or unrecognized command format: {command}")

    return True


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Python Match-Case Test Started ---\n")

    test_payloads = [
        ["add", "Laptop", 2],
        ["delete", 404, 505],
        Order("Wireless Headphones", 1, "shipped"),
        Order("Coffee Maker", 1, "pending"),
        {"type": "invoice", "amount": 1250.50},
        ["invalid_command_format"],  # Missing parameters
        "EXIT"
    ]

    for payload in test_payloads:
        print(f"Input: {payload}")
        should_continue = process_command(payload)
        print("-" * 45)
        if not should_continue:
            break
