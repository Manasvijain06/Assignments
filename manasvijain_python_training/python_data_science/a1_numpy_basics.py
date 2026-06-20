import numpy as np

# 1.Create Numpy array
arr = np.array([10,20,30,40,50])

# 2.Perform Mean, Max, Min, Sum
print("Mean:",arr.mean())
print("Max:",arr.max())
print("Min:",arr.min())
print("Sum:",arr.sum())

# 3.Create two arrays
arr_1 = np.array([1, 2, 3])
arr_2 = np.array([4, 5, 6])

print("Addition of arr_1 & arr_2 :",arr_1 + arr_2)
print("Multiplication of arr_1 & arr_2 :",arr_1 * arr_2)

# 4.Create a 3×3 matrix using NumPy
matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])

print("3x3 Matrix:")
print(matrix)
