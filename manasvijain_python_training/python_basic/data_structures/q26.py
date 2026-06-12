""" Question 26 : Count even and odd numbers in a list."""

def count_even_odd(numbers: list[int]) -> tuple[int, int]:
    """
    Count even and odd numbers in a list.
    """
    even_count  = 0
    odd_count = 0

    for num in numbers:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    return even_count, odd_count

if __name__ == "__main__":
    number = [10,24,56,45,35,8,97,4,63]
    even_count, odd_count = count_even_odd(number)
    print(f"Even numbers count: {even_count}")
    print(f"Odd numbers count: {odd_count}")