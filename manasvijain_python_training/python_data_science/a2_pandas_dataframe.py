import pandas as pd

# Create a Dataframe for employees
def get_employee_data():
    employees = {
        "Name": ["Rahul", "Priya", "Amit", "Anuj"],
        "Age": [25, 30, 28, 35],
        "Department": ["HR", "IT", "Finance", "IT"],
        "Salary": [30000, 50000, 45000, 60000]
    }
    return pd.DataFrame(employees)

def main():
    df = get_employee_data()

    # 1.Show first 2 rows
    print("First 2 Rows:")
    print(df.head(2))

    # 2.Show summary statistics
    print("\nSummary Statistics:")
    print(df.describe())

    # 3.Display only IT employees
    print("\nIT Employees:")
    print(df[df["Department"]=="IT"])

    # 4.Add Bonus column
    df["Bonus"] = df["Salary"] * 0.10

    print("\nDataFrame with Bonus Column:")
    print(df)

if __name__ == "__main__":
    main()