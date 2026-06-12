"""
Question 17 : Write a function to calculate square of a number.
"""

def calculate_square(number: int) -> int:
    """
    Calculate and return the square of a number.
    """
    return number * number

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    square = calculate_square(number)
    print(f"Square of {number} is: {square}")