# Question 12 : Write a generator to produce Fibonacci numbers.

from typing import Generator

def fibonacci_series(limit: int) -> Generator[int, None, None]:
    """
    Generate Fibonacci numbers up to a given count.

    Args:
        limit: Number of Fibonacci terms to generate.

    Yields:
        int: Next Fibonacci number in the sequence.
    """
    first_number: int = 0
    second_number: int = 1

    for _ in range(limit):
        yield first_number

        first_number, second_number = second_number, first_number + second_number

if __name__ == "__main__":
    limit = int(input("Enter the limit:"))
    print("\n--- Fibonacci series ---")
    for number in fibonacci_series(limit):
        print(number)
