# Question 37 : Create a module with two utility functions and import it into another Python file.

"""
Utility functions module.
"""


def add_numbers(first_number: int, second_number: int) -> int:
    """
    Return the sum of two numbers.

    Args:
        first_number: First integer.
        second_number: Second integer.

    Returns:
        int: Sum of both numbers.
    """
    return first_number + second_number


def multiply_numbers(first_number: int, second_number: int) -> int:
    """
    Return the product of two numbers.

    Args:
        first_number: First integer.
        second_number: Second integer.

    Returns:
        int: Product of both numbers.
    """
    return first_number * second_number