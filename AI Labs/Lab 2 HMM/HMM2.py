import sys

# Input data block containing matrix dimensions and elements
input_data = sys.stdin.read()

# Split input data into lines
input_lines = input_data.splitlines()
iterator = iter(input_lines)

# Function to read matrix from input
# Edited: Changed from NumPy array to standard Python list representation
def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]]  # All elements from index 2 and forward converted into floats
    matrix = [elements[i * cols:(i + 1) * cols] for i in range(rows)]  # Reshape list into 2D list (matrix)
    return matrix

# Function to read emission sequence from input
def read_emission_sequence(iterator):
    line = next(iterator).split()
    sequence = [int(value) for value in line[1:]]
    return sequence

# Function to perform the Viterbi algorithm
def viterbi(A, B, pi, T_sequence):
    N = len(A)
    T = len(T_sequence)
    delta = [[0.0 for _ in range(N)] for _ in range(T)] 
    delta_idx = [[0 for _ in range(N)] for _ in range(T)] 
    
    # Initialize delta for the first time step
    O_initial = T_sequence[0]
    for i in range(N):
        delta[0][i] = pi[0][i] * B[i][O_initial]
    
    # Loop through each time step
    for t in range(1, T):
        O_current = T_sequence[t]
        for i in range(N):
            max_transition_prob = float('-inf')
            max_state = 0
            for j in range(N):
                transition_prob = A[j][i] * delta[t-1][j] 
                if transition_prob > max_transition_prob:
                    max_transition_prob = transition_prob
                    max_state = j
            delta[t][i] = max_transition_prob * B[i][O_current] 
            delta_idx[t][i] = max_state 
    
    # Backtrack to find the most probable path
    path = [0 for _ in range(T)]  
    path[T - 1] = max(range(N), key=lambda i: delta[T - 1][i])  
    
    for t in range(T - 2, -1, -1):
        path[t] = delta_idx[t + 1][path[t + 1]]  
    
    return path

# Read matrices and emission sequence from input
A = read_matrix(iterator) 
B = read_matrix(iterator)  
pi = read_matrix(iterator)  
T_sequence = read_emission_sequence(iterator)

# Perform Viterbi algorithm and calculate the most probable path
path = viterbi(A, B, pi, T_sequence)

# Print the result
clean_path = " ".join(map(str, path))
print(f"{clean_path}")

"""
import sys
import numpy as np

input_data = """#4 4 0.0 0.8 0.1 0.1 0.1 0.0 0.8 0.1 0.1 0.1 0.0 0.8 0.8 0.1 0.1 0.0 
#4 4 0.9 0.1 0.0 0.0 0.0 0.9 0.1 0.0 0.0 0.0 0.9 0.1 0.1 0.0 0.0 0.9 
#1 4 1.0 0.0 0.0 0.0 
#4 1 1 2 2 
"""

input_lines = input_data.splitlines()
iterator = iter(input_lines)

def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]]
    matrix = np.array(elements).reshape(rows, cols)
    return matrix

def read_emission_sequence(iterator):
    line = next(iterator).split()
    sequence = [int(value) for value in line[1:]]
    return sequence

A = read_matrix(iterator)
B = read_matrix(iterator)
pi = read_matrix(iterator)
T_sequence = read_emission_sequence(iterator)

def viterbi(A, B, pi, T_sequence):
    N = A.shape[0]
    T  = len(T_sequence)
    delta = np.zeros((T,N))
    O_initial = T_sequence[0]

    #Initializing t=1
    for i in range(N):
        delta[0, i] = pi[0, i] * B[i, O_initial]
        delta_idx = np.zeros((T, N), dtype=int) #To keep track of the state indices leading to the max value
    
    #Looping through every t
    for t in range(1, T):
        O_current = T_sequence[t]

        #For every state i per t
        for i in range(N):
            max_transition_prob = float('-inf')
            max_state = 0 #Stores the index of the previous state (j) that gives the maximum value

            #We check the probabilities in t-1 that lead to state i
            for j in range(N):
                transition_prob = A[j, i] * delta[t-1, j]
                if transition_prob > max_transition_prob: #and save the path with the largest transition probability 
                    max_transition_prob = transition_prob
                    max_state = j #as well as the index for the state the path moves through
            
            #Finally storing the value at time step t, state i
            delta[t, i] = max_transition_prob * B[i, O_current] 
            delta_idx[t, i] = max_state 
    
    path = np.zeros(T, dtype=int)
    path[T - 1] = np.argmax(delta[T - 1, :])  # Start from the state with the highest probability at time T-1

    for t in range(T - 2, -1, -1): #from T-2 to 0
        path[t] = delta_idx[t + 1, path[t + 1]] #the index of the previous state that led to the state we chose at time t + 1

    return path

path = viterbi(A, B, pi, T_sequence)
clean_path = " ".join(map(str, path))
print(f"{clean_path}")

"""
