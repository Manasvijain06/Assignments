# Question 10 : Write a custom iterator class that returns numbers from 1 to N.

class NumberIterator:
    """
    Custom iterator that returns numbers from 1 to N.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.current = 1

    def __iter__(self) -> "NumberIterator":
        return self

    def __next__(self) -> int:
        if self.current > self.limit:
            raise StopIteration

        value = self.current
        self.current += 1
        return value

if __name__ == "__main__":
    n = int(input("Enter N: "))

    if n < 1:
        print("Please enter a positive number.")
    else:
        for number in NumberIterator(n):
            print(number)