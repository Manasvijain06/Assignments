from q33 import check_prime

# Pytest test cases for is_prime function.

def test_prime_number() -> None:
    """
    Test with a known prime number.
    """
    assert check_prime(7) is True


def test_non_prime_number() -> None:
    """
    Test with a known non-prime number.
    """
    assert check_prime(8) is False


def test_edge_case_one() -> None:
    """
    Test edge case: 1 is not a prime number.
    """
    assert check_prime(1) is False


def test_edge_case_zero() -> None:
    """
    Test edge case: 0 is not a prime number.
    """
    assert check_prime(0) is False


def test_negative_number() -> None:
    """
    Test negative numbers (not prime).
    """
    assert check_prime(-5) is False