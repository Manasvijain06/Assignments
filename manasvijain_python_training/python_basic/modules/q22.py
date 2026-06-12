"""
Questions 22 : Use math module to find square root, power, and factorial.
"""
import math

def calculate_square_root(number: int) -> float:
    """
    Calculate and return the square root of a number.
    """
    return math.sqrt(number)

def calculate_power(base: int, exponent: int) -> float:
    """
    Calculate and return the power of a number.
    """
    return math.pow(base, exponent)

def calculate_factorial(number: int) -> int:
    """
    Calculate and return the factorial of a number.
    """
    return math.factorial(number)

if __name__ == "__main__":
    number = int(input("Enter a number to find square root and factorial: "))
    base = int(input("Enter the base number: "))
    exponent = int(input("Enter the exponent: "))

    print(f"Square root of {number} is: {calculate_square_root(number)}")

    print(f"{base} raised to the power {exponent} is: {calculate_power(base, exponent)}")

    print(f"Factorial of {number} is: {calculate_factorial(number)}")
