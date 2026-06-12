""" Question 27 : Reverse a list without using reverse()."""

def reverse_list(numbers: list[int]) -> list[int]:
    """
    Return the reversed list.
    """

    return numbers[::-1]

if __name__ == "__main__":
    numbers = [10, 25, 8, 40, 15]

    reversed_numbers = reverse_list(numbers)

    print(f"Original List: {numbers}")
    print(f"Reversed List: {reversed_numbers}")