# Question 40 : Create a package for mathematical operations and use it.


from math_operations import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
)

# CONSTANTS
FIRST_NUMBER: int = 20
SECOND_NUMBER: int = 10


if __name__ == "__main__":
    print(f"Addition: {add_numbers(FIRST_NUMBER, SECOND_NUMBER)}")

    print(f"Subtraction: {subtract_numbers(FIRST_NUMBER, SECOND_NUMBER)}")

    print(f"Multiplication: {multiply_numbers(FIRST_NUMBER, SECOND_NUMBER)}")

    print(f"Division: {divide_numbers(FIRST_NUMBER, SECOND_NUMBER)}")