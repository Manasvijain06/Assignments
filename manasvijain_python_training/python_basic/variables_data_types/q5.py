"""question 5 : Write a program to swap two numbers."""

def swap_numbers(first_number: int, second_number: int) -> None:
    """Swap and display two numbers."""
    print(f"Before swapping: first_number = {first_number}, second_number = {second_number}")
    first_number, second_number = second_number, first_number
    print(f"After swapping: first_number = {first_number}, second_number = {second_number}")

if __name__ == "__main__":
    try:
        first_number = int(input("Enter the first number: "))
        second_number = int(input("Enter the second number: "))
        swap_numbers(first_number, second_number)
    except ValueError:
        print("Please enter valid integers.")