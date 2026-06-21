# Question 29 : Replace multiple spaces in a string with a single space using re.sub().

import re

def remove_extra_spaces(text: str) -> str:
    """
    Replace multiple spaces with a single space.

    Args:
        text: Input string.

    Returns:
        str: String with extra spaces removed.
    """
    return re.sub(r"\s+", " ", text).strip()


if __name__ == "__main__":
    sentence: str = ("Python    is   a    powerful      language.")

    cleaned_sentence: str = remove_extra_spaces(sentence)

    print(f"Original : '{sentence}'")
    print(f"Cleaned  : '{cleaned_sentence}'")