# Question 25 : Write a regular expression to validate an email address.

import re

def is_valid_email(email: str) -> bool:
    """
    validate a email address.

    Args:
        email: email to validate.

    Returns:
        bool: True if valid, otherwise False.
    """
    email_pattern = (r"^[\w\.-]+@[\w\.-]+\.\w+$")

    return bool(re.match(email_pattern, email))

if __name__ == "__main__":
    email = input("Enter an email address:")

    if is_valid_email(email):
        print("Valid email address.")
    else:
        print("Invalid email address.")