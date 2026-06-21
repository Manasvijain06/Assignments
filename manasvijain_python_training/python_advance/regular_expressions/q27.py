# Question 27 :  Use re.search() to check whether a word exists in a sentence.

import re

def contains_word(sentence: str, word: str) -> bool:
    """
    Check whether a word exists in a sentence.

    Args:
        sentence: Input sentence.
        word: Word to search for.

    Returns:
        bool: True if the word exists, otherwise False.
    """
    return bool(re.search(re.escape(word), sentence))

if __name__ == "__main__":
    sentence: str = ("Python is a powerful programming language.").lower()

    word: str = input("Enter word to search:").lower()

    if contains_word(sentence, word):
        print("Word found.")
    else:
        print("Word not found.")