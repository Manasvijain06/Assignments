""" Question 38 : Copy content from one file to another."""

SOURCE_FILE = "name.txt"
DESTINATION_FILE = "copy.txt"

def copy_file_content(source_file: str, destination_file: str) -> None:
    """Copy content from one file to another."""

    with open(source_file, "r", encoding="utf-8") as src:
        content = src.read()

    with open(destination_file, "w", encoding="utf-8") as dest:
        dest.write(content)

if __name__ == "__main__":
    copy_file_content(SOURCE_FILE, DESTINATION_FILE)
    print(f"Content copied from {SOURCE_FILE} to {DESTINATION_FILE} successfully.")