# Question 3 : Write a program using try-except-else-finally to read a number from a file  and print its square.

FILE_NAME: str = "number.txt"

def read_number_from_file(file_name: str) -> float:
    """
    Read a number from a file.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return float(file.read().strip())

def calculate_square(number:float) -> float:
    """
    Calculate the square of a number.
    """
    return number ** 2

if __name__ == "__main__":
    try:
        number = read_number_from_file(FILE_NAME)

    except FileNotFoundError:
        print("File not found.")

    except ValueError:
        print("File does not contain valid number.")

    else:
        square = calculate_square(number)
        print(f"Square: {square}")

    finally:
        print("Program execution completed.")
