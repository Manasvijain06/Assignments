"""Question 32 : Create a student dictionary and access values."""

def access_student_details(student: dict[str, str | int]) -> None:
    """Access and display dictionary values."""

    print(f"Student Name: {student['name']}")
    print(f"Student Age: {student['age']}")
    print(f"Student Course: {student['course']}")

if __name__ == "__main__":
    student = {"name": "Manasvi","age": 20,"course": "Python"}
    access_student_details(student)