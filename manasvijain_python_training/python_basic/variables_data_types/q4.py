"""Question 4 : Create variables of type int, float, string, and boolean. Print their types using type()."""

INTEGER_VALUE: int = 42
FLOAT_VALUE: float = 3.14
STRING_VALUE: str = "Hello, Python!"
BOOLEAN_VALUE: bool = True

def display_variable_types() -> None:
    """Display the data types of the variables."""   
    print(f"Type of INTEGER_VALUE: {type(INTEGER_VALUE)}")
    print(f"Type of FLOAT_VALUE: {type(FLOAT_VALUE)}")
    print(f"Type of STRING_VALUE: {type(STRING_VALUE)}")
    print(f"Type of BOOLEAN_VALUE: {type(BOOLEAN_VALUE)}")

if __name__ == "__main__":
    display_variable_types()