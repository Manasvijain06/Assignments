# Question 22 : Write a recursive function to calculate Fibonacci.

def calculate_fibonacci(position: int) -> int:
    """
    Calculate the Fibonacci number at a given position using recursion.

    Args:
        number: Position in the Fibonacci sequence.

    Returns:
        int: Fibonacci number at the given position.
    """
    if position <= 1:
        return position

    return (calculate_fibonacci(position - 1) + calculate_fibonacci(position - 2))


if __name__ == "__main__":
    position: int = int(input("Enter Fibonacci position : "))

    result: int = calculate_fibonacci(position)

    print(f"Fibonacci Number: {result}")