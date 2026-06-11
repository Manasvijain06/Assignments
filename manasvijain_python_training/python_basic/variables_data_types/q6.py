"""question 6 : Take two numbers and print sum, difference, multiplication, and division."""

def perform_arithmetic_operations(num1: float, num2: float) -> None:
    """Display arithmetic operations on two numbers."""
    print(f"Sum: {num1 + num2}")
    print(f"Difference: {num1 - num2}")
    print(f"Multiplication: {num1 * num2}")
    print(f"Division: {num1 / num2 }")

if __name__ == "__main__":
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        perform_arithmetic_operations(num1, num2)
    except ValueError:
        print("Please enter valid numbers.")
    except ZeroDivisionError:
        print("Cannot divide by zero.")