# Question 20 : Use reduce() to find the product of all elements in a list.

from functools import reduce

# CONSTANTS
NUMBERS: list[int] = [1, 2, 3, 4, 5]


def get_product(numbers: list[int]) -> int:
    """
    Find the product of all elements in a list using reduce().

    Args:
        numbers: List of integers.

    Returns:
        int: Product of all elements.
    """
    return reduce(lambda first_number, second_number: first_number * second_number, numbers)


if __name__ == "__main__":
    result: int = get_product(NUMBERS)

    print(f"Original Number: {NUMBERS}")
    print(f"Product: {result}")