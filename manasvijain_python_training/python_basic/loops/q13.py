"""questions 13 : Print multiplication table of a number."""

def print_multiplication_table(number: int) -> None:
    """
    Print multiplication table of a number.
    """

    print(f"Multiplication Table of {number}:")
    for i in range(1, 11):
        result = number * i
        print(f"{number} x {i} = {result}")

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    print_multiplication_table(number)