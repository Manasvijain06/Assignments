"""Question 14 : Find factorial of a number."""

def factorial(number: int) -> None:
    """Calculate and display the factorial of a number."""

    factorial = 1
    
    for current_number in range(1, number + 1):
        factorial *= current_number

    print(f"Factorial of {number} is : {factorial}")

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    factorial(number)