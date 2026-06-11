"""question 9 : Find the largest of three numbers."""

def find_largest(num1: int, num2: int, num3: int) -> None:
    """Find and display the largest of three numbers."""

    if (num1 >= num2 and num1 >= num3):
        print(f"Largest Number: {num1}")

    elif (num2 >= num1 and num2 >= num3):
        print(f"Largest Number: {num2}")

    else:
        print(f"Largest Number: {num3}")

if __name__ == "__main__":
    num1 = int(input("Enter the first number: "))
    num2 = int(input("Enter the second number: "))
    num3 = int(input("Enter the third number: "))
    find_largest(num1, num2, num3)