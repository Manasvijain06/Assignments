# Question 31 : Create a password validation program using regex (minimum length, one digit, one special character).

import re


def is_valid_password(password: str) -> bool:
    """
    Validate a password.

    Conditions:
    - Minimum 8 characters
    - At least one digit
    - At least one special character

    Args:
        password: Password to validate.

    Returns:
        bool: True if valid, otherwise False.
    """
    password_pattern: str = r"^(?=.*\d)(?=.*[!@#$%^&*()_\-+={}[\]|:;\"'<>,.?/~`]).{8,}$"

    return bool(re.match(password_pattern, password))


if __name__ == "__main__":
    password: str = input("Enter a password: ")

    if is_valid_password(password):
        print("Valid password.")
    else:
        print("Invalid password.")