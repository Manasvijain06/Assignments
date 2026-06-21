# Question 18 : Use map() to convert a list of numbers into their squares.


# CONSTANTS
NUMBERS: list[int] = [1, 2, 3, 4, 5]


def get_square_numbers(numbers: list[int]) -> list[int]:
    """
    Convert a list of numbers into their squares using map().

    Args:
        numbers: List of integers.

    Returns:
        list[int]: List containing square values.
    """

    return list(map(lambda number: number ** 2, numbers))


if __name__ == "__main__":
    result: list[int] = get_square_numbers(NUMBERS)
    print(f"Original Numbers: {NUMBERS}")

    print(f"Squared Numbers: {result}")