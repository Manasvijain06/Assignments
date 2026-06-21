from q32 import add_numbers

#Pytest test cases for addition of two numbers.

def test_add_positive_number() -> None:
    """
    Verify addition of positive numbers.
    """

    assert add_numbers(2,3) == 5

def test_add_negative_number() -> None:
    """
    Verify addition of negative numbers.
    """

    assert add_numbers(-2,-3) == -5

def test_add_mixed_numbers() -> None:
    """
    Verify addition of positive & negative numbers.
    """

    assert add_numbers(5, -3) == 2

def test_add_zero() -> None:
    """
    Verify addition of numbers with zero.
    """

    assert add_numbers(0, 10) == 10


