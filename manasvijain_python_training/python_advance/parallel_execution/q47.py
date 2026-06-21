# Question 47 : Convert a normal function into parallel execution using ThreadPoolExecutor.

from concurrent.futures import ThreadPoolExecutor


# CONSTANTS
NUMBERS: list[int] = [1, 2, 3, 4, 5]

def calculate_square(number: int) -> int:
    """
    Calculate the square of a number.

    Args:
        number: Input number.

    Returns:
        int: Square of the number.
    """
    return number ** 2


if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        results = executor.map(calculate_square, NUMBERS)

    for result in results:
        print(result)