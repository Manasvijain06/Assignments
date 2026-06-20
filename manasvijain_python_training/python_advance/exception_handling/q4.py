# Question 4 : Handle multiple exceptions  in a single program.

def divide_numbers(dividend: float, divisor: float) -> float:
    """
    Divide two numbers.

    Args:
        dividend: Number to be divided.
        divisor: Number used as divisor.

    Returns:
        float: division result.
    """
    return dividend / divisor


if __name__ == "__main__":
    try:
        first_number = float(input("Enter first number: "))
        second_number = float(input("Enter second number: "))

        result = divide_numbers(first_number, second_number)

        print(f"Result: {result}")

    except ValueError:
        print("Invalid input. Please enter numeric values.")

    except ZeroDivisionError:
        print("Cannot divide by zero.")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")