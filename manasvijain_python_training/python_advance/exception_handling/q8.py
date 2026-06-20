# Question 8 : Write a program that handles FileNotFoundError when trying to open a file.

FILE_NAME: str = "new.txt"

def read_file(file_name: str) -> str:
    """
    Read and return the content of a file.

    Args:
        file_name: Name of the file to read.

    Returns:
        str: Content of the file.
    """
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    try:
        file_content = read_file(FILE_NAME)
        print(file_content)

    except FileNotFoundError:
        print("File not found.")