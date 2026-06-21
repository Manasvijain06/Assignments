# Question 17 : Write a lambda function to find the square of a number.

def get_square(number: int) -> int:
    """
    Calculate the square of a number using a lambda function.

    Args:
        number: Number to square.

    Returns:
        int: Square of the number.
    """
    square = lambda value: value ** 2

    return square(number)


if __name__ == "__main__":
    number: int = int(input("Enter a number: "))

    result: int = get_square(number)

    print(f"Square: {result}")