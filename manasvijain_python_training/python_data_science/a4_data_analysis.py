import pandas as pd
from a2_pandas_dataframe import get_employee_data

# get employees DataFrame
df = get_employee_data()

# Average salary by department
print("Average Salary by Department:")
print(df.groupby("Department")["Salary"].mean())

# Maximum salary by department
print("\nMaximum Salary by Department:")
print(df.groupby("Department")["Salary"].max())

# Count employees per department
print("\nEmployee Count by Department:")
print(df.groupby("Department")["Name"].count())
