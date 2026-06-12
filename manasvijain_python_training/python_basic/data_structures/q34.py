"""Question 34 : Merge two dictionaries."""

def merge_dictionaries(dict1: dict, dict2: dict) -> None:
    """Merge two dictionaries."""

    #method 1: Using the update() method
    merged_dict = dict1.copy()  # Create a copy of the first dictionary
    merged_dict.update(dict2)   # Update with the second dictionary

    print(f"Merged Dictionary: {merged_dict}")

    #method 2: Using | operator 
    merged_dict_2 = dict1 | dict2  
    print(f"Merged Dictionary using | operator: {merged_dict_2}")

if __name__ == "__main__":
    dict1 = {"a": 1, "b": 2, "c": 3}
    dict2 = {"d": 4, "e": 5, "f": 6}

    merge_dictionaries(dict1, dict2)