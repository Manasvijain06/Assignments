"""Question 15 : Reverse a number using loop."""

def reverse_number(number: int) -> None:
    """
    Reverse a number using loop.
    """
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = (reversed_number * 10) + digit
        number //= 10

    print(f"Reversed Number: {reversed_number}")

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    reverse_number(number)