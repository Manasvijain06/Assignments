""" Question 29 : Convert tuple into list and modify it."""

def convert_and_modify_tuple(number: tuple[int,...]) -> list[int]:
    """ Convert a tuple into a list and modify it."""
    number_list = list(numbers)
    number_list.append(60)
    number_list[0] = 100
    
    return number_list
    
if __name__ == "__main__":
    numbers = (10, 20, 30, 40, 50)
    modified_list = convert_and_modify_tuple(numbers)
    
    print(f"Original Tuple: {numbers}")
    print(f"Modified List: {modified_list}")