"""Question 30 : Perform union, intersection, and difference on two sets."""

def perform_set_operations(set1: set[int], set2: set[int]) -> None:
    """
    Perform union, intersection, and difference on two sets.
    """

    print(f"First Set: {set1}")
    print(f"Second Set: {set2}")
    
    print(f"Union: {set1.union(set2)}")
    print(f"Intersection: {set1.intersection(set2)}")
    print(f"Difference: {set1.difference(set2)}")

if __name__ == "__main__":
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}

    perform_set_operations(set1, set2)
    