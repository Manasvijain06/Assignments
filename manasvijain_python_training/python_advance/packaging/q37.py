"""
Import and use utility functions from another module.
"""

from q37_utility import add_numbers, multiply_numbers

# CONSTANTS
FIRST_NUMBER: int = 10
SECOND_NUMBER: int = 5


if __name__ == "__main__":
    addition_result: int = add_numbers(
        FIRST_NUMBER,
        SECOND_NUMBER,
    )

    multiplication_result: int = multiply_numbers(
        FIRST_NUMBER,
        SECOND_NUMBER,
    )

    print(f"Sum: {addition_result}")
    print(f"Product: {multiplication_result}")