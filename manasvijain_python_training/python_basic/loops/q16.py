"""Question 16 : Check whether a number is prime."""

def check_prime_number(number: int) -> None:
    """
    Check whether a number is prime.
    """

    if number < 2:
        print(f"{number} is not a prime number.")
        return

    for i in range(2, number):
        if number % i == 0:
            print(f"{number} is not a prime number.")
            return

    print(f"{number} is a prime number.")

if __name__ == "__main__":
    number = int(input("Enter a number: "))
    check_prime_number(number)