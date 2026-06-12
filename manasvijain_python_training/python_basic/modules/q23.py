"""Question 23 : Generate random numbers using random module."""

import random

def generate_random_number(start: int, end: int) -> int:
    """
    Generate and display a random number.
    """

    return random.randint(start, end)

if __name__ == "__main__":
    start = int(input("Enter start range: "))
    end = int(input("Enter end range: "))
    random_number = generate_random_number(start, end)
    print(f"Random number: {random_number}")