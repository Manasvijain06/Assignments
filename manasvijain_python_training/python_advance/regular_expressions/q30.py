# Question 30 : Write a pattern to check if a string contains only alphabets.

import re


def contains_only_alphabets(text: str) -> bool:
    """
    Check whether a string contains only alphabets.

    Args:
        text: Input string.

    Returns:
        bool: True if the string contains only alphabets,
        otherwise False.
    """
    return bool(re.fullmatch(r"[A-Za-z]+", text))


if __name__ == "__main__":
    text: str = input("Enter a string: ")

    if contains_only_alphabets(text):
        print("String contains only alphabets.")
    else:
        print("String contains characters other than alphabets.")