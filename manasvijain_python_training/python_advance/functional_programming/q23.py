# Question 23 : Convert a simple  loop-based program into a functional style using map or filter.

# CONSTANTS
NAMES: list[str] = ["manasvi", "diya", "priya"]


def convert_to_uppercase(names: list[str]) -> list[str]:
    """
    Convert names to uppercase using map().

    Args:
        names: List of names.

    Returns:
        list[str]: Uppercase names.
    """
    return list(map(lambda name: name.upper(), names))


if __name__ == "__main__":
    result: list[str] = convert_to_uppercase(NAMES)

    print(result)