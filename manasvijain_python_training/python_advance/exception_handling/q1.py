# Write a program that takes a number as input and handles ValueError if the input is not a valid integer.

def get_user_input() -> str:
    """Get input from the user."""
    return input("Enter a number: ")


def convert_to_integer(user_input: str) -> int:
    """Convert string input to an integer."""
    return int(user_input)


if __name__ == "__main__":
    try:
        user_input = get_user_input()
        number = convert_to_integer(user_input)
        print("You entered:", number)
    except ValueError:
        print("Invalid input! Please enter a valid integer.")
