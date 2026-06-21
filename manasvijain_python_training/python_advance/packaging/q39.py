# Question 39 : Create a package with two modules and include an __init__.py file.

"""
Use functions from string_package.
"""

from string_package import (convert_to_uppercase, convert_to_lowercase,)

# CONSTANTS
TEXT: str = "Hello World"


if __name__ == "__main__":
    print(f"Uppercase: {convert_to_uppercase(TEXT)}")

    print(f"Lowercase: {convert_to_lowercase(TEXT)}")