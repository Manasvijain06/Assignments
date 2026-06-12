"""Question 37 : Append data to existing file"""

FILE_NAME = "name.txt"

def append_to_file(filename: str, text: str) -> None:
    """Append data to an existing file."""
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"\n{text}")

if __name__ == "__main__":
    user_data = input("Enter data to append to the file: ")
    append_to_file(FILE_NAME, user_data)
    print("Data appended successfully.")