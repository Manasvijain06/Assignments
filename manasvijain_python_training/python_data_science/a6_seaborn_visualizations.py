import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from a2_pandas_dataframe import get_employee_data

df = get_employee_data()

# 1. Barplot: Department vs Salary
sns.barplot(data=df, x="Department", y="Salary")
plt.title("Department vs Salary")
plt.show()

# 2. Boxplot: Salary Distribution
sns.boxplot(y=df["Salary"])
plt.title("Salary Distribution")
plt.show()

# 3. Heatmap: Correlation between Age and Salary
correlation = df[["Age", "Salary"]].corr()

sns.heatmap(correlation, annot=True)
plt.title("Correlation Heatmap")
plt.show()