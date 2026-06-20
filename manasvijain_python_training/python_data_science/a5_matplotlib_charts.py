import matplotlib.pyplot as plt

# Data
departments = ["HR", "IT", "Finance"]
employees = [5, 12, 7]

# 1.Create Bar Chart
plt.figure()
plt.bar(departments, employees)
plt.title("Employees by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.show()

# 2.Create Line Chart
plt.figure()
plt.plot(departments, employees, marker="o")
plt.title("Employees by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.show()

# 3. Histogram
salaries = [30000, 40000, 50000, 60000, 45000]

plt.figure()
plt.hist(salaries)
plt.title("Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Frequency")
plt.show()

# 4. Scatter Plot
ages = [25, 30, 28, 35]
salaries = [30000, 50000, 45000, 60000]

plt.figure()
plt.scatter(ages, salaries)
plt.title("Age vs Salary")
plt.xlabel("Age")
plt.ylabel("Salary")
plt.show()