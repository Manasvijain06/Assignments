""" question 31 : Remove duplicates from list using set."""

def remove_duplicate(number: list[int]) -> list[int]:
    """Remove duplicates from the list."""

    return list(set(number))

if __name__ == "__main__":
    number = [10, 22, 8, 43, 15, 22, 8, 50, 43, 10]

    unique_numbers = remove_duplicate(number)

    print(f"Original List: {number}")
    print(f"List without duplicates: {unique_numbers}")