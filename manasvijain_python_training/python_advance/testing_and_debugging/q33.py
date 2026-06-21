# Question 33 :Write pytest test cases for a function that checks whether a number is prime.

def check_prime(number: int) -> bool:
    """
    Check whether a number is prime.

    Args:
        number: Number to check.

    Returns:
        bool: True if prime, else False.
    """
    if number <= 1:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True