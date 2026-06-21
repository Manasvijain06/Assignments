# QUestion 11 :Generator function that yields square numbers up to N.

def generate_square_numbers(limit: int):
    """
    Generator that yields square numbers from 1 to limit.

    Yields:
        int: Square of numbers from 1 to limit.
    """
    for number in range(1, limit + 1):
        yield number ** 2


if __name__ == "__main__":
    limit = int(input("Enter N: "))

    print("\n--- Squares ---")

    if limit < 1:
        print("Please enter a positive number.")
    else:
        for square in generate_square_numbers(limit):
            print(square)

