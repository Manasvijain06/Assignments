# Question 21 : Write a recursive function to calculate factorial.


def calculate_factorial(number: list) -> int:
    """
    Calculate the factorial of a number using recursion.

    Args:
        number: Non-negative integer.

    Returns:
        int: Factorial of the number.
    """
    if number == 0 or number == 1:
        return 1

    return number * calculate_factorial(number - 1)


if __name__ == "__main__":
    number: int = int(input("Enter a number: "))

    result: int = calculate_factorial(number)

    print(f"Factorial: {result}")