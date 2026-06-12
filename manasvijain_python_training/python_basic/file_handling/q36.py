"""Question 36 :  Read a file and count words, lines, and characters."""

def count_file_contents(file_name: str) -> tuple[int, int, int]:
    """Count words, lines, and characters in a file."""

    with open(file_name, "r") as file:
        content = file.read()

    word_count = len(content.split())
    line_count = len(content.splitlines())
    character_count = len(content)

    return word_count, line_count, character_count


if __name__ == "__main__":
    words, lines, characters = count_file_contents("name.txt")

    print(f"Words: {words}")
    print(f"Lines: {lines}")
    print(f"Characters: {characters}")