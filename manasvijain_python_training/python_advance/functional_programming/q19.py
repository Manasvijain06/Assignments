# Question 19 : Use filter() to extract even numbers from a list.

# CONSTANTS
NUMBERS: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def get_even_numbers(numbers: list[int]) -> list[int]:
    """
    Extract even numbers from a list using filter().

    Args:
        numbers: List of integers.

    Returns:
        list[int]: List containing even numbers.
    """
    return list(filter(lambda number: number % 2 == 0,numbers))


if __name__ == "__main__":
    result: list[int] = get_even_numbers(NUMBERS)
    print(f"Original List Numbers: {NUMBERS}")

    print(f"Even Numbers: {result}")