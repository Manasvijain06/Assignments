# Question 26 : Write a regular expression to validate a 10-digit mobile number.

import re

def is_valid_mobile_number(number: str) -> bool:
    """
    Validate a 10-digit mobile number.

    Args:
        mobile_number: Mobile number to validate.

    Returns:
        bool: True if valid, otherwise False.
    """
    mobile_pattern: str = r"^\d{10}$"

    return bool(re.match(mobile_pattern, number))

if __name__ == "__main__":
    number = input("Enter an mobile number:")

    if is_valid_mobile_number(number):
        print("Valid mobile number.")
    else:
        print("Invalid mobile number.")