"""question 7 : Write a program to check whether a number is even or odd."""

def check_even_odd(number: int) -> None:
    """Check whether a number is even or odd."""
    
    if number % 2 == 0:
        print(f"{number} is even.")
    else:
        print(f"{number} is odd.")

if __name__ == "__main__":
    try:
        number = int(input("Enter a number: "))
        check_even_odd(number)
    except ValueError:
        print("Please enter a valid integer.")