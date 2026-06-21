# Question 34 : Create a function with a logical bug and use pdb to identify the issue.

"""
Create a function with a logical bug and use pdb to identify the issue.
"""

import pdb

def divide_numbers(a: int, b: int) -> float:
    """
    Divide and return two numbers.
    """
    result = a * b
    return result


if __name__ == "__main__":
    x = 10
    y = 5

    pdb.set_trace()  # Debugger starts here

    output = divide_numbers(x, y)
    print(f"Result: {output}")