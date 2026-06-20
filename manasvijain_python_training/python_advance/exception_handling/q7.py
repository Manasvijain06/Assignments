# Question 7 : Create a custom exception called AgeException and raise it if age is less than 18.

class AgeException(Exception):
    """
    Custom exception raised when age is less than 18.
    """

def validate_age(age: int) -> None:
    """
    Validate that the age is at least 18.

    Args:
        age: Age to validate.

    Returns:
        int: The validated age.

    Raises:
        AgeException: If age is less than 18.
    """
    if age < 18:
        raise AgeException("Age must be 18 or older.")


if __name__ == "__main__":
    try:
        user_age = int(input("Enter your age: "))

        validate_age(user_age)

        print(f"Valid age")

    except AgeException as error:
        print(error)

    except ValueError:
        print("Please enter a valid age.")