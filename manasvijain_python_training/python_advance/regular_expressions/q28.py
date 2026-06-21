# Question 27 :  Use re.findall() to extract all words starting with a capital letter.

import re


def extract_capital_words(text: str) -> list[str]:
    """
    Extract all words starting with a capital letter.

    Args:
        text: Input string.

    Returns:
        list[str]: List of words starting with a capital letter.
    """
    return re.findall(r"\b[A-Z][a-zA-Z]*\b", text)


if __name__ == "__main__":
    sentence: str = ("I am Manasvi Jain,")

    capital_words: list[str] = extract_capital_words(sentence)

    print(f"Capital Words: {capital_words}")