"""Question 3 : Take user input (name and age) and print a formatted message."""

def display_user_information(user_name: str,user_age: int) -> None:
    """Display user information in a message."""
    print(f"Hello {user_name}, you are {user_age} years old.")

if __name__ == "__main__":
    try:
        user_name = input("Enter your name: ")
        user_age = int(input("Enter your age: "))
        display_user_information(user_name, user_age)
    except ValueError:
        print("Please enter a valid input.")