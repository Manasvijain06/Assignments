# Question 9 :  Create an iterator for a list and print elements using next().

def create_iterator(data_list: list) -> iter:
    """
    Create an iterator from a list.

    Args:
        data_list: List of elements.

    Returns:
        iterator: Iterator object of the list.
    """
    return iter(data_list)

if __name__ == "__main__":
    number = [10,20,30,40,50]

    iterator = create_iterator(number)

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))