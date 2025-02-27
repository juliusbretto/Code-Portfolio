import sys
import numpy as np

input_data = """4 4 0.4 0.2 0.2 0.2 0.2 0.4 0.2 0.2 0.2 0.2 0.4 0.2 0.2 0.2 0.2 0.4 
4 4 0.4 0.2 0.2 0.2 0.2 0.4 0.2 0.2 0.2 0.2 0.4 0.2 0.2 0.2 0.2 0.4 
1 4 0.241896 0.266086 0.249153 0.242864 
1000 0 1 2 3 3 0 0 1 1 1 2 2 2 3 0 0 0 1 1 1 2 3 3 0 0 0 1 1 1 2 3 3 0 1 2 3 0 1 1 1 2 3 3 0 1 2 2 3 0 0 0 1 1 2 2 3 0 1 1 2 3 0 1 2 2 2 2 3 0 0 1 2 3 0 1 1 2 3 3 3 0 0 1 1 1 1 2 2 3 3 3 0 1 2 3 3 3 3 0 1 1 2 2 3 0 0 0 0 0 0 0 0 0 1 1 1 1 1 2 2 2 3 3 3 3 0 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 3 3 3 0 1 2 3 0 1 1 1 2 3 0 1 1 2 2 2 2 2 3 0 1 1 1 2 2 2 2 3 0 0 0 0 0 1 1 1 1 2 2 3 3 0 1 2 3 3 0 0 0 0 0 0 1 1 2 2 3 0 0 1 1 1 1 1 1 2 3 3 0 0 1 1 1 2 3 0 0 1 2 3 0 1 1 2 3 3 0 0 0 1 2 3 3 3 0 1 1 1 1 2 3 3 3 3 3 3 0 1 2 2 2 2 2 2 3 0 1 1 1 2 2 3 3 3 3 0 1 2 3 0 0 0 1 1 2 2 3 0 0 0 0 0 0 0 1 2 2 2 3 3 3 3 0 0 1 2 2 2 3 3 3 0 0 1 2 2 3 0 0 0 0 1 1 1 2 3 3 3 3 3 3 3 3 0 1 2 3 0 0 1 2 3 3 3 0 0 0 0 0 1 1 1 1 2 3 0 0 0 1 2 2 3 3 0 0 0 1 1 1 1 1 2 3 3 3 3 0 1 1 1 2 2 3 0 1 2 3 3 3 3 0 0 0 0 1 2 3 3 0 1 2 2 3 3 0 0 1 1 2 3 3 0 1 2 2 3 3 3 0 0 1 1 2 3 3 3 3 0 0 1 1 2 3 3 0 1 2 3 0 1 1 2 2 3 0 1 2 3 3 0 1 1 1 2 2 2 3 3 0 0 1 1 1 1 1 2 3 3 3 0 1 1 2 2 2 2 3 3 0 0 1 2 3 0 1 1 2 2 2 2 3 0 0 1 2 2 3 0 0 0 0 0 1 1 1 2 3 0 0 1 2 3 3 0 0 0 1 2 2 2 3 3 0 0 0 1 2 2 2 2 2 3 0 1 1 2 3 0 0 1 1 1 2 2 3 0 0 0 0 1 1 1 2 2 3 0 1 1 1 2 2 2 3 3 0 0 1 2 2 3 3 3 0 1 1 2 3 0 0 0 0 0 1 2 2 2 3 3 3 0 0 0 1 2 3 0 1 1 2 3 3 3 0 1 2 2 2 3 0 0 1 1 1 1 2 3 3 0 0 0 0 1 2 3 3 3 0 0 0 1 1 2 3 0 1 1 1 1 2 2 2 2 2 2 3 0 0 0 0 1 2 2 2 2 3 0 1 2 2 3 0 1 2 3 0 1 2 3 0 0 0 1 1 2 2 3 3 0 1 1 1 1 2 2 3 3 0 1 1 1 2 2 2 3 3 3 0 1 1 2 3 3 0 1 2 3 0 0 0 0 1 2 3 0 0 0 0 0 0 1 2 2 3 3 0 0 1 2 3 0 1 2 2 3 0 0 0 1 1 2 2 2 2 2 3 3 3 3 3 0 1 2 2 3 3 3 3 3 0 0 1 1 2 2 3 0 0 1 2 2 3 3 3 0 0 0 1 2 2 2 2 3 3 0 1 2 3 0 0 1 1 1 2 2 3 0 0 1 1 2 2 2 3 3 0 0 1 1 1 1 1 2 3 3 3 0 1 2 2 2 2 3 3 3 3 3 3 0 0 0 0 0 0 1 2 3 0 0 1 1 1 2 3 0 0 1 1 2 2 2 2 3 3 3 0 1 1 2 2 2 3 3 0 0 0 0 0 0 1 2 2 3 3 0 0 0 0 0 0 1 2 3 3 3 0 1 1 1 2 2 2 2 2 3 3 3 0 1 2 2 2 3 3 3 3 0 0 0 0 1 2 3 3 3 3 3 3 0 0 1 1 1 1 2 3 0 1 2 3 0 1 1 2 3 3 3 0 0 0 0 1 1 2 3 3 3 3 0 0 1 1 1 2 2 2 2 2 2 3 3 0 0 0 1 2 3 0 0 1 1 2 2 3 3 3 3 3 0 0 1 2 2 2 2 3 0 0 1 1 1 1 1 2 3 3 0 0 1 1 1 2 3 3 3 0 0 
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
print(f"pi: {pi},\n A: {A}\n, B: {B}")
T_sequence = read_emission_sequence(iterator)

def alpha_pass(A, B, pi, T_sequence):
    N = A.shape[0]
    T = len(T_sequence)
    alpha = np.zeros((T, N))
    T_1 = T_sequence[0]
    print("pi3: ", pi)

    for i in range(N):
        alpha[0, i] = pi[0, i] * B[i, T_1] 
        #First row (0) initialized through iterating over initial probabilities (pi-values) multiplied by B(i|M_1), i.e. the probability of observing M_1 given state i
        if alpha[0, i] == 0:
            print(f"Initial alpha[0, {i}] is zero, pi[0, {i}] = {pi[0, i]}, B[{i}, {T_1}] = {B[i, T_1]}")


    for t in range(1, T): 
        T_t = T_sequence[t] #Current emission (observation) at each time step (observations can be playing, barking, napping etc)
        for k in range(N): #Iterating over every possible state for time t (Xt) (states can be active, bored, sleepy etc)
            alpha[t, k] = B[k, T_t] * sum(alpha[t-1, i] * A[i, k] for i in range(N)) 
            #if alpha[t, k] == 0:
                #print(f"Alpha[{t}, {k}] is zero at time t={t}, state k={k}")
    
    
    final_probability = sum(alpha[T-1, i] for i in range(N))
    print("Final probability: ", final_probability)

    return alpha, final_probability
    
def beta_pass(A, B, T_sequence):
    N = A.shape[0]  
    T = len(T_sequence)  
    beta = np.zeros((T, N))

    beta[T - 1, :] = 1  #Initializing beta_T(i) = 1 for all i (the last row of beta). Set the last row to 1
    
    #Recursively compute beta values moving backwards in time
    for t in range(T - 2, -1, -1):
        O_t_plus_1 = T_sequence[t + 1]  #Next observation in the sequence
        for i in range(N):  #Iterate over each state at time t
            beta[t, i] = sum(A[i, j] * B[j, O_t_plus_1] * beta[t + 1, j] for j in range(N))
            #if beta[t, i] == 0:
                #print(f"Beta[{t}, {i}] is zero at time t={t}, state i={i}")

    return beta
    
def di_gamma_calc(alpha, beta, A, B, T_sequence, total_probability):
    T = len(T_sequence)
    N = A.shape[0]
    
    di_gamma = np.zeros((T - 1, N, N))
    
    for t in range(T - 1):
        for i in range(N):  #Iterate over each state at time t
            for j in range(N):  #Iterate over each state at time t+1
                numerator = alpha[t, i] * A[i, j] * B[j, T_sequence[t + 1]] * beta[t + 1, j]
                
                di_gamma[t, i, j] = numerator / total_probability if total_probability != 0 else 0
                
    return di_gamma

def gamma_calc(di_gamma):
    T = len(T_sequence)
    N = A.shape[0]
    gamma = np.zeros((T, N))
    
    for t in range(T-1):
        for i in range(N):
            gamma[t, i] = np.sum(di_gamma[t, i, :])

    #Last step, calculate gamma_T(i) which is the sum over all di-gamma values from time T-2
    for i in range(N):
        gamma[T-1, i] = np.sum(di_gamma[T - 2, :, i])
    
    return gamma

def estimate_lambda(gamma, di_gamma, T_sequence, N, M):
    T = len(T_sequence)

    #Update transition matrix A
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            numerator = np.sum(di_gamma[:, i, j])
            denominator = np.sum(gamma[:-1, i])  #Gamma values from time 0 to T-2
            A[i, j] = numerator / denominator if denominator != 0 else 0

    #Update emission matrix B
    B = np.zeros((N, M))
    for j in range(N):
        for k in range(M):
            numerator = np.sum([gamma[t, j] for t in range(T - 1) if T_sequence[t] == k])
            denominator = np.sum(gamma[:-1, j])
            B[j, k] = numerator / denominator if denominator != 0 else 0

    #Update initial state probabilities pi
    pi = gamma[0, :].reshape(1, -1)  #The initial probabilities are equal to the gamma values at time 0 (and reshaped to avoid complation issues)

    return A, B, pi

def baum_welch(A, B, pi, T_sequence, iterations=100, tolerance=1e-6):
    N = A.shape[0]
    M = B.shape[1]
    print("pi2: ", pi)
    

    for iteration in range(iterations):
        #Run alpha and beta passes
        alpha, final_probability = alpha_pass(A, B, pi, T_sequence)
        beta = beta_pass(A, B, T_sequence)

        #Compute di-gamma and gamma values
        di_gamma = di_gamma_calc(alpha, beta, A, B, T_sequence, final_probability)
        gamma = gamma_calc(di_gamma)

        #Estimate lambda
        A_new, B_new, pi_new = estimate_lambda(gamma, di_gamma, T_sequence, N, M)

        #Check for convergence; if no --> iterate again, reestimate lambda etc
        if np.max(abs(A_new - A)) < tolerance and np.max(abs(B_new - B)) < tolerance:
            break

        #Update parameters for the next iteration
        A, B, pi = A_new, B_new, pi_new

    return A, B, pi

"""
alpha, total_prob = alpha_pass(A, B, pi, T_sequence)
beta = beta_pass(A, B, T_sequence)
di_gamma = di_gamma_calc(alpha, beta, A, B, T_sequence, total_prob)
gamma = gamma_calc(di_gamma)

print(alpha)
print(beta)
print(total_prob)

Q, W, E = estimate_lambda(gamma, di_gamma, T_sequence, A.shape[0], B.shape[1])
"""

def format_output(matrix):
    rows, cols = matrix.shape
    elements = ' '.join(f'{matrix[r, c]:.6g}' for r in range(rows) for c in range(cols))
    return f'{rows} {cols} {elements}'

A_opt, B_opt, pi_opt = baum_welch(A, B, pi, T_sequence)

A_formatted = format_output(A_opt)
B_formatted = format_output(B_opt)

print(A_formatted)
print(B_formatted)

"""
import sys

input_data = sys.stdin.read()

input_lines = input_data.splitlines()
iterator = iter(input_lines)

def read_matrix(iterator):
    line = next(iterator).split()
    rows = int(line[0])
    cols = int(line[1])
    elements = [float(value) for value in line[2:]]
    matrix = [elements[i * cols:(i + 1) * cols] for i in range(rows)]
    return matrix

def read_emission_sequence(iterator):
    line = next(iterator).split()
    sequence = [int(value) for value in line[1:]]
    return sequence

def alpha_pass(A, B, pi, T_sequence):
    N = len(A)
    T = len(T_sequence)
    alpha = [[0.0 for _ in range(N)] for _ in range(T)]
    T_1 = T_sequence[0]
    for i in range(N):
        alpha[0][i] = pi[0][i] * B[i][T_1]
    for t in range(1, T):
        T_t = T_sequence[t]
        for k in range(N):
            alpha[t][k] = B[k][T_t] * sum(alpha[t-1][i] * A[i][k] for i in range(N))
    final_probability = sum(alpha[T-1][i] for i in range(N))
    return alpha, final_probability

def beta_pass(A, B, T_sequence):
    N = len(A)  
    T = len(T_sequence)  
    beta = [[0.0 for _ in range(N)] for _ in range(T)]
    for i in range(N):
        beta[T - 1][i] = 1.0
    for t in range(T - 2, -1, -1):
        O_t_plus_1 = T_sequence[t + 1]
        for i in range(N):
            beta[t][i] = sum(A[i][j] * B[j][O_t_plus_1] * beta[t + 1][j] for j in range(N))
    return beta

def estimate_lambda(alpha, beta, A, B, T_sequence):
    T = len(T_sequence)
    N = len(A)
    M = len(B[0])
    gamma = [[0.0 for _ in range(N)] for _ in range(T)]
    di_gamma = [[[0.0 for _ in range(N)] for _ in range(N)] for _ in range(T - 1)]
    
    for t in range(T - 1):
        denom = sum(alpha[t][i] * beta[t][i] for i in range(N))
        for i in range(N):
            gamma[t][i] = (alpha[t][i] * beta[t][i]) / denom if denom != 0 else 0.0
            for j in range(N):
                di_gamma[t][i][j] = (alpha[t][i] * A[i][j] * B[j][T_sequence[t + 1]] * beta[t + 1][j]) / denom if denom != 0 else 0.0
    denom = sum(alpha[T - 1][i] * beta[T - 1][i] for i in range(N))
    for i in range(N):
        gamma[T - 1][i] = (alpha[T - 1][i] * beta[T - 1][i]) / denom if denom != 0 else 0.0
    
    A_new = [[0.0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        denom = sum(gamma[t][i] for t in range(T - 1))
        for j in range(N):
            numer = sum(di_gamma[t][i][j] for t in range(T - 1))
            A_new[i][j] = numer / denom if denom != 0 else 0.0
    
    B_new = [[0.0 for _ in range(M)] for _ in range(N)]
    for i in range(N):
        denom = sum(gamma[t][i] for t in range(T))
        for k in range(M):
            numer = sum(gamma[t][i] for t in range(T) if T_sequence[t] == k)
            B_new[i][k] = numer / denom if denom != 0 else 0.0
    
    return A_new, B_new

A = read_matrix(iterator)
B = read_matrix(iterator)
pi = read_matrix(iterator)
T_sequence = read_emission_sequence(iterator)

alpha, total_prob = alpha_pass(A, B, pi, T_sequence)
beta = beta_pass(A, B, T_sequence)
A_est, B_est = estimate_lambda(alpha, beta, A, B, T_sequence)

def format_output(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    elements = ' '.join(f"{value:.6g}" for row in matrix for value in row)
    return f"{rows} {cols} {elements}"

print(format_output(A_est))
print(format_output(B_est))

"""