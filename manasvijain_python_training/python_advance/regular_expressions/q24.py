# Question 24 : Write a program to extract all numbers from a given string using regular expressions.

import re

def extract_all_numbers(text: str) -> list[str]:
    """
    Extract all numbers from a string.

    Args:
        text: Input String
    Return:
        list[str]:List of numbers found in a string.
    """
    return re.findall(r"\d+",text)

if __name__ == "__main__":

    text = "My age is 25 and my score is 98."

    number = extract_all_numbers(text)

    print(f"Numbers found: {number}")