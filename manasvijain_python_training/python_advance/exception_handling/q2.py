# Question 2 : Write a program to divide two numbers entered by the user and handle ZeroDivisionError.

def divide_numbers(dividend: float, divisor: float) -> float:
    """
    Divide two numbers.
    Args:
        dividend: Number to be divided.
        divisor: Number used as divisor.

    Returns:
        float: Division result.
    """

    return dividend / divisor


if __name__ == "__main__":
    try:
        first_number = float(input("Enter first number: "))
        second_number = float(input("Enter second number: "))

        result = divide_numbers(first_number, second_number)

        print(f"Result: {result}")

    except ZeroDivisionError:
        print("Cannot divide by zero.")

    except ValueError:
        print("Please enter valid numeric values.")