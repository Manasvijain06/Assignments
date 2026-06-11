"""Question 2 : Write a program to check your Python version."""

import sys

def display_python_version() -> None:
    """Display the current Python version."""
    print(f"Python Version: {sys.version}")

if __name__ == "__main__":
    display_python_version()