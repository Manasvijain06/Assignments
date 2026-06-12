""" Question 40 : Create a Student class with attributes and display details."""

class Student:
    """ Represent a student."""

    def __init__(self,name: str,age: int,course: str) -> None:
        """Initialize student attributes."""
        self.name = name
        self.age = age
        self.course = course

    def display_details(self) -> None:
        """Display student details."""
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Course: {self.course}")

if __name__ == "__main__":
    student = Student("Manasvi", 20, "python")
    student.display_details()