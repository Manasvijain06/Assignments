"""questions 8 : Check whether a number is positive, negative, or zero."""

def check_number_sign(number: int) -> None:
    """ check whether a number is positive, negative or zero."""

    if number > 0:
        print(f"{number} is positive.")
    elif number < 0:
        print(f"{number} is negative.")
    else:
        print("The number is zero.")

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    check_number_sign(number)