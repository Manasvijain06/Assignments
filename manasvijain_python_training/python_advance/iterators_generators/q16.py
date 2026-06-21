# Question 16 : Show an example of a built-in generator (like range) and iterate over it.

def iterate_range() -> None:
    for number in range(1, 6):
        print(number)

if __name__ == "__main__":

    print("Built-in generator (range):")

    iterate_range()