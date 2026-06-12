"""
Question 18 : Write a function to check palindrome(Number and string).
"""

def is_number_palindrome(number: int) -> bool:
    """
    Check whether a number is a palindrome.
    """

    number_as_string = str(number)
    return number_as_string == number_as_string[::-1]

def is_string_palindrome(text: str) -> bool:
    """
    Check whether a string is a palindrome.
    """

    return text == text[::-1]

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    text = input("Enter a string: ")

    if is_number_palindrome(number):
        print(f"{number} is a palindrome number.")
    else:
        print(f"{number} is not a palindrome number.")
        
    if is_string_palindrome(text):
        print(f"'{text}' is a palindrome string.")
    else:
        print(f"'{text}' is not a palindrome string.")