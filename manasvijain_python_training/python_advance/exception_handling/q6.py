# Question 6 : Create a function that raises a ValueError if a number is negative.

def validate_number(number: int) -> None:
    """Validate that a number is non-negative. """

    if number < 0:
        raise ValueError("Negative numbers are not allowed.")

if __name__ == "__main__":
    try:
        value = int(input("Enter a number:"))

        validate_number(value)

        print(f"This is a Valid number.")

    except ValueError as error:
        print(error)


