import pandas as pd

# Create the dataset
data = {
    "Name":["Rahul","Priya","Anuj"],
    "Age":[25,None,29],
    "Salary":[30000,40000,None]
}

df = pd.DataFrame(data)
print(df)

# 1.Detect missing values
print("Missing Values:")
print(df.isnull())

# 2.Replace missing Age with mean
df["Age"] = df["Age"].fillna(df["Age"].mean())

# 3.Replace missing Salary with 0
df["Salary"] = df["Salary"].fillna(0)

print("\nUpdated DataFrame:")
print(df)