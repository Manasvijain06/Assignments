"""Question 33 : Count frequency of characters in a string using dictionary."""

def count_character_frequency(text: str) -> dict[str, int]:
    """Count frequency of characters in a string."""
    
    frequency = {}

    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    return frequency    

if __name__ == "__main__":
    text = input("Enter a string: ")
    result = count_character_frequency(text)
    print(f"Character Frequency in '{text}': {result}")