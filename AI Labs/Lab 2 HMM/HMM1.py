import sys

#Input data block containing matrix dimensions and elements
input_data = sys.stdin.read()

#Split input data into lines
input_lines = input_data.splitlines()
iterator = iter(input_lines)

#Function to read matrix from input
def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]]  # All elements from index 2 and forward converted into floats
    matrix = [elements[i * cols:(i + 1) * cols] for i in range(rows)]  # Reshape list into 2D list (matrix)
    return matrix

#Function to read emission sequence from input
def read_emission_sequence(iterator):
    line = next(iterator).split()
    sequence = [int(value) for value in line[1:]]
    return sequence

# Function to perform the alpha pass
def alpha_pass(A, B, pi, T_sequence):
    N = len(A)
    T = len(T_sequence)
    alpha = [[0.0 for _ in range(N)] for _ in range(T)]
    
    # Initialize alpha for the first time step
    T_1 = T_sequence[0]
    for i in range(N):
        alpha[0][i] = pi[0][i] * B[i][T_1]
    
    # Compute alpha for each time step
    for t in range(1, T):
        T_t = T_sequence[t]
        for k in range(N):
            alpha[t][k] = B[k][T_t] * sum(alpha[t-1][i] * A[i][k] for i in range(N))
    
    # Sum the final probabilities
    final_probability = sum(alpha[T-1][i] for i in range(N))
    
    return final_probability

# Read matrices and emission sequence from input
A = read_matrix(iterator) 
B = read_matrix(iterator) 
pi = read_matrix(iterator)
T_sequence = read_emission_sequence(iterator)

# Perform alpha pass and calculate the probability
probability = alpha_pass(A, B, pi, T_sequence)

# Print the result
print(f"{probability:.6f}")


"""


import sys
import numpy as np

input_data = """#4 4 0.0 0.8 0.1 0.1 0.1 0.0 0.8 0.1 0.1 0.1 0.0 0.8 0.8 0.1 0.1 0.0 
#4 4 0.9 0.1 0.0 0.0 0.0 0.9 0.1 0.0 0.0 0.0 0.9 0.1 0.1 0.0 0.0 0.9 
#1 4 1.0 0.0 0.0 0.0 
#8 0 1 2 3 0 1 2 3 
"""

input_lines = input_data.splitlines()
iterator = iter(input_lines)

def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]] #All elements from index 2 and forward converted into floats
    matrix = np.array(elements).reshape(rows, cols) #Reshapes the matrix into a numpy array with given row and col size
    return matrix

def read_emission_sequence(iterator):
    line = next(iterator).split()
    sequence = [int(value) for value in line[1:]]
    return sequence

A = read_matrix(iterator)
B = read_matrix(iterator)
pi = read_matrix(iterator)
T_sequence = read_emission_sequence(iterator)

def alpha_pass(A, B, pi, T_sequence):
    N = A.shape[0]
    T = len(T_sequence)
    alpha = np.zeros((T, N))
    T_1 = T_sequence[0]
    for i in range(N):
        alpha[0, i] = pi[0, i] * B[i, T_1] #First row (0) initialized through iterating over initial probabilities (pi-values) multiplied by B(i|M_1), i.e. the probability of observing M_1 given state i

    for t in range(1, T): 
        T_t = T_sequence[t] #Current emission (observation) at each time step (observations can be playing, barking, napping etc)
        for k in range(N): #Iterating over every possible state for time t (Xt) (states can be active, bored, sleepy etc)
            alpha[t, k] = B[k, T_t] * sum(alpha[t-1, i] * A[i, k] for i in range(N)) 
            #B[k, T_t] is the emission probability of emitting the current observation (T_t) given that we are in state k
            #alpha[j-1, i]: The probability of being in state i at the previous time step (j-1)
            #A[i, k]: The transition probability of moving from state i to state k
            #So: Multiply the emission probability (B[k, T_t]) by the sum (total probability) of getting to state k from any of the previous states
    
    final_probability = sum(alpha[T-1, i] for i in range(N)) #Finally the probabilities in the last step are summed, giving the probability of observing the sequence
    #(Sum all α values at the final time step (T-1) for all possible states (i from 0 to N-1))

    return final_probability

probability = alpha_pass(A, B, pi, T_sequence)

print(f"{probability:.6f}")


"""

