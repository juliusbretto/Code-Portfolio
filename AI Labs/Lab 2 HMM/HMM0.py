import sys

input_data = sys.stdin.read()

input_lines = input_data.splitlines()
iterator = iter(input_lines)

def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]]  #All elements from index 2 and forward converted into floats
    matrix = [elements[i * cols:(i + 1) * cols] for i in range(rows)] #Convert the 1D input into a 2D matrix
    return matrix

def matrix_multiply(matrix1, matrix2):
    rows_matrix1 = len(matrix1) 
    cols_matrix1 = len(matrix1[0]) 
    rows_matrix2 = len(matrix2)
    cols_matrix2 = len(matrix2[0])
    
    if cols_matrix1 != rows_matrix2: 
        raise ValueError("Cannot multiply matrices: incompatible dimensions.")
    
    result = [[0.0 for _ in range(cols_matrix2)] for _ in range(rows_matrix1)] #Creates 2D matrix with 0.0 in every cell which will hold the result
    
    #Matrix multiplication
    #Each row element for matrix1 is multiplied with corresponding column element of matrix2 and then summed, the resulting value stored in result
    for i in range(rows_matrix1): #Iterates over the rows of matrix1 (result row index)
        for j in range(cols_matrix2): #Iterates over the columns of matrix2 (result column index)
            for k in range(cols_matrix1): #Iterates over elements in the current row of matrix1 and the current column of matrix2, multiplying elements and accumulating their product.
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    
    return result

#Formatting the matrix so that the output is according to the specification on Kattis
def format_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    elements = ' '.join(f"{value:.6g}" for row in matrix for value in row)
    return f"{rows} {cols} {elements}"

A = read_matrix(iterator)
B = read_matrix(iterator)
pi = read_matrix(iterator)

pi_A = matrix_multiply(pi, A)
result = matrix_multiply(pi_A, B)

print(format_matrix(result))

"""
import sys
import numpy as np

#input_data = 4 4 0.2 0.5 0.3 0.0 0.1 0.4 0.4 0.1 0.2 0.0 0.4 0.4 0.2 0.3 0.0 0.5 
#                4 3 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0 0.2 0.6 0.2
#                1 4 0.0 0.0 0.0 1.0

input_lines = input_data.splitlines()
iterator = iter(input_lines)

def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]] #All elements from index 2 and forward converted into floats
    matrix = np.array(elements).reshape(rows, cols) #Reshapes the matrix into a numpy array with given row and col size
    return matrix

A = read_matrix(iterator)
B = read_matrix(iterator)
pi = read_matrix(iterator)

output = np.dot(np.dot(pi, A), B)

output_rows, output_cols = output.shape
output_cleaned = ' '.join(f"{value:.6g}" for value in output.flatten()) #Flattens the 1D-matrix into a numpy array, and for each value limits to one decimal as well as joins them together to a string with a " " between

print(f"{output_rows} {output_cols} {output_cleaned}")


## REVISED WITHOUT NUMPY ##
"""