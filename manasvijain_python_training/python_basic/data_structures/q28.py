""" Question 28 : Create a tuple and access elements."""

def create_and_access_tuple(my_tuple: tuple[int, ...]) -> None:

    """Create a tuple and access its elements."""
    
    print("Tuple:", my_tuple)
    print("First element:", my_tuple[0])
    print("Second element:", my_tuple[1])
    print("Third element:", my_tuple[2])
    print("Fourth element:", my_tuple[3])

if __name__ == "__main__":
    my_tuple = (1,2,3,4,5,6,7,8,9,10)
    create_and_access_tuple(my_tuple)