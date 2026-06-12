"""Question 42 : Implement inheritance using Person and Employee class."""

class Person:

    def __init__(self,name: str,age: int) -> None:
        self.name = name
        self.age = age

    def introduce(self) -> None:
        print(f"My name is {self.name} and age is {self.age}.")


class Employee(Person):
    
    def __init__(self,name: str,age: int,employee_id: str) -> None:
        super().__init__(name, age)
        self.employee_id = employee_id

    def display_employee(self) -> None:
        print(f"Employee ID: {self.employee_id}")

if __name__ == "__main__":
    employee = Employee("Manasvi Jain", 20, "101")
    employee.introduce()
    employee.display_employee()