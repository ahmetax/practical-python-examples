# Author: Ahmet Aksoy
# Date: 21.05.2026
# Python3.12 Ubuntu 24.04

"""
Advanced Type Hinting Example
Demonstrates Python 3.12+ Generic Type Parameter Syntax (PEP 695)
combined with data validation concepts.
"""

from typing import Generic, TypeVar
from dataclasses import dataclass

# 1. Modern Python 3.12+ Type Alias Syntax
# We define a custom type that can be either an integer or a string
type Identifier = int | str

# 2. Python 3.12+ New Generic Syntax
# Instead of old TypeVar declarations, we can use the new syntax directly.
# This generic class handles API responses for any data type 'T'.
class APIResponse[T]:
    def __init__(self, status: str, data: T, error: str | None = None) -> None:
        self.status: str = status
        self.data: T = data
        self.error: str | None = error

    def is_successful(self) -> bool:
        return self.status == "success"


# 3. Strongly Typed Data Structures
@dataclass
class User:
    id: Identifier
    username: str
    email: str


@dataclass
class Product:
    id: Identifier
    title: str
    price: float


# 4. Functions leveraging precise Type Hints
def process_user_response(response: APIResponse[User]) -> None:
    """Processes an API response specifically containing User data."""
    if response.is_successful():
        user: User = response.data
        print(f"Success: Processing User #{user.id} -> {user.username} ({user.email})")
    else:
        print(f"Error occurred: {response.error}")


def process_product_response(response: APIResponse[Product]) -> None:
    """Processes an API response specifically containing Product data."""
    if response.is_successful():
        product: Product = response.data
        print(f"Success: Processing Product #{product.id} -> {product.title} costs ${product.price:.2f}")
    else:
        print(f"Error occurred: {response.error}")


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Advanced Type Hinting Test Started ---\n")

    # Creating a successful User response
    user_data = User(id=101, username="ahmet_dev", email="ahmet@example.com")
    user_api_call = APIResponse(status="success", data=user_data)
    
    # Python 3.12 static type checkers (like mypy) will know exactly 
    # that user_api_call.data is of type 'User'
    process_user_response(user_api_call)
    print("-" * 50)

    # Creating a successful Product response (using a string identifier)
    product_data = Product(id="PROD-99X", title="Mechanical Keyboard", price=89.99)
    product_api_call = APIResponse(status="success", data=product_data)
    
    process_product_response(product_api_call)
    print("-" * 50)

    # Creating a failed response scenario
    failed_api_call: APIResponse[User] = APIResponse(
        status="fail", 
        data=None, 
        error="User not found"
    )
    process_user_response(failed_api_call)
