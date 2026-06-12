"""Question 39 : Search a word in a file."""

FILE_NAME = "name.txt"

def search_word_in_file(file_name: str,search_word: str) -> bool:
    """Search for a word in a file."""

    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()

    return search_word.lower() in content.lower()


if __name__ == "__main__":
    word_to_search = input("Enter the word to search: ")

    is_word_found = search_word_in_file(FILE_NAME,word_to_search)

    if is_word_found:
        print(f'"{word_to_search}" found in the file.')
    else:
        print(f'"{word_to_search}" not found in the file.')