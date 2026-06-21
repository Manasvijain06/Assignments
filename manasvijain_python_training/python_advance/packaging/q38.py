#Question 38 : Explain the difference between a module and a package with an example.

"""
Module:
- A module is a single Python file (.py) that contains functions,
classes, or variables.
- It helps organize and reuse code.

Example:
    calculator.py

    def add_numbers(a, b):
        return a + b

Usage:
    from calculator import add_numbers


Package:
- A package is a collection of related modules organized in a directory.
- A package must contain an __init__.py file.

Example:

    math_package/
    ├── __init__.py
    ├── addition.py
    └── subtraction.py

addition.py:
    def add_numbers(a, b):
        return a + b

subtraction.py:
    def subtract_numbers(a, b):
        return a - b

Usage:
    from math_package.addition import add_numbers


Difference:

Module:
    - Single Python file.
    - Used to organize related code in one file.

Package:
    - Directory containing multiple modules.
    - Used to organize large projects into multiple modules.

Conclusion:
A module is a single .py file, whereas a package is a folder
containing multiple modules and an __init__.py file.
"""