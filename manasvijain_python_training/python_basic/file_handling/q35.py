""" Question 35 : Create a file and write your name into it."""

def write_name_to_file(filename: str, name: str) -> None:
    """Write a name to a file.
    Args:
        filename (str): The name of the file to write to.
        name (str): The name to write into the file.
    """

    with open(filename, "w",encoding="utf-8") as file:
        file.write(name)

if __name__ == "__main__":
    filename = "name.txt"
    name = input("Enter your name: ")
    write_name_to_file(filename, name)
    print(f"Your name has been written to {filename}.")