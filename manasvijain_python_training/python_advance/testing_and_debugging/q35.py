# Question 35 :  Use pdb breakpoints inside a loop and inspect variable values.

import pdb

def calculate_total(numbers: list[int]) -> None:
    """
    Calculate and display the running total of numbers.
    """
    total = 0

    for number in numbers:
        pdb.set_trace()  # Breakpoint inside loop

        total += number

        print(f"Number: {number}, Total: {total}")


if __name__ == "__main__":
    values = [10, 20, 30, 40]

    calculate_total(values)