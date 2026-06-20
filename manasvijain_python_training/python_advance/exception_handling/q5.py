# Question 5 : Write a program that catches all exceptions and prints the error message.

def divide_10_by_num(num: int) -> float:
    """
    Divide two numbers and return result.
    """
    return 10 / num


if __name__ == "__main__":
    try:
        num = int(input("Enter second number: "))

        result = divide_10_by_num(num)

        print(f"Result: {result}")

    except Exception as e:
        print(f"Error occurred: {e}")