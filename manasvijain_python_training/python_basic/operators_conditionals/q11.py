"""question 11 : Check whether a year is a leap year."""

def check_leap_year(year: int) -> None:
    """Check and display whether a year is a leap year."""

    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        print(f"{year} is a leap year.")
    else:
        print(f"{year} is not a leap year.")

if __name__ == "__main__":
    year = int(input("Enter a year: "))
    check_leap_year(year)
