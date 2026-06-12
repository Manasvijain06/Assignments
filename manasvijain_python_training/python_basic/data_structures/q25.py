""" Question 25 : Create a list of 10 numbers and find sum, max, sort it, and remove duplicates."""

def perform_list_operations(numbers: list[int]) -> None:
    """
    Perform various operations on a list.
    """

    print(f"Original List: {numbers}")
    print(f"Sum: {sum(numbers)}")
    print(f"Maximum Number: {max(numbers)}")
    print(f"Sorted List: {sorted(numbers)}")
    print(f"List Without Duplicates: {list(set(numbers))}")

if __name__ == "__main__":
    numbers = [10, 25, 8, 40, 15, 25, 8, 50, 60, 10]

    perform_list_operations(numbers)