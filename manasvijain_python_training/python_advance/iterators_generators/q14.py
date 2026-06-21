# Question 14 : Explain the difference between iterator and generator with a small example.

"""
Iterator:
- An iterator is an object that allows elements to be accessed one at a time.
- It is created using iter() and accessed using next().
- It raises StopIteration when no elements are left.

Generator:
- A generator is a function that uses the yield keyword.
- It automatically creates an iterator.
- Generators are memory efficient because they do not store all values at once.
"""


def demonstrate_iterator() -> None:
    """
    Demonstrate an iterator example.
    """

    numbers = [10, 20, 30]

    # iter() creates an iterator
    # from the given collection.
    iterator = iter(numbers)

    print("Iterator Output:")

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
# next(iterator) now will raise stopIteration

def demonstrate_generator():
    """
    Demonstrate a generator example.
    """
    for i in range(5):
        yield i


if __name__ == "__main__":

    print("\n--- Iterator Output: ")
    demonstrate_iterator()

    print("\nGenerator Output:")
    for value in demonstrate_generator():
        print(value)
