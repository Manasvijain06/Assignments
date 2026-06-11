""" question 10 : Calculate grade based on marks (A/B/C/Fail)."""

def calculate_grade(marks: float) -> None:
    """Calculate and display grade based on marks."""
    if marks >= 90:
        print("Grade: A")
    elif marks >= 75:
        print("Grade: B")
    elif marks >= 60:
        print("Grade: C")
    else:
        print("Grade: Fail")

if __name__ == "__main__":
    marks = float(input("Enter your marks: "))
    calculate_grade(marks)
