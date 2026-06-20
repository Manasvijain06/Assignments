import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create Student Dataset
students = {
    "Name": ["Rahul", "Priya", "Siri", "Anuj"],
    "Marks": [70, 80, 90, 60],
    "Hours Studied": [2, 3, 5, 1]
}

# 1.Load into Pandas DataFrame
df = pd.DataFrame(students)

# 2.Add Performance Column
df["Performance"] = np.where(df["Marks"] > 65, "Pass", "Fail")

print("Student Data:")
print(df)

# 3.Line Chart: Hours vs Marks
plt.figure(figsize=(6, 4))
plt.plot(df["Hours Studied"], df["Marks"], marker="o")
plt.title("Hours vs Marks")
plt.xlabel("Hours Studied")
plt.ylabel("Marks")
plt.show()

# Scatter Plot: Hours Studied vs Marks
plt.figure(figsize=(6, 4))
plt.scatter(df["Hours Studied"], df["Marks"])
plt.title("Study vs Marks")
plt.xlabel("Study hours")
plt.ylabel("Marks")
plt.show()

# 4.Seaborn Barplot: Performance vs Marks
plt.figure(figsize=(6, 4))
sns.barplot(data=df, x="Performance", y="Marks")
plt.title("Performance vs Marks")
plt.show()