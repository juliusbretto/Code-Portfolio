import sys
import numpy as np
import math
import time

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
#print(f"pi: {pi},\n A: {A}\n, B: {B}")
T_sequence = read_emission_sequence(iterator)

def alpha_pass(A, B, pi, T_sequence):
    N = len(A)
    T = len(T_sequence)

    # Initialize alpha with the first observation
    alpha = []
    alpha_t0 = []
    for state in range(N):
        alpha_t0.append(pi[0][state] * B[state][T_sequence[0]])
    # Normalize the first step
    scaler_0 = 1 / sum(alpha_t0)
    alpha_t0 = [value * scaler_0 for value in alpha_t0]
    alpha.append(alpha_t0)
    scalers = [scaler_0]

    # Iteratively compute alpha for each time step
    for t in range(1, T):
        alpha_t = []
        for curr_state in range(N):
            sum_prob = 0
            for prev_state in range(N):
                sum_prob += alpha[t-1][prev_state] * A[prev_state][curr_state]
            alpha_t.append(sum_prob * B[curr_state][T_sequence[t]])
        # Normalize the current alpha_t
        scaler_t = 1 / sum(alpha_t)
        alpha_t = [value * scaler_t for value in alpha_t]
        alpha.append(alpha_t)
        scalers.append(scaler_t)

    return alpha, scalers
    
def beta_pass(A, B, T_sequence, scalers):
    N = len(A)
    T = len(T_sequence)
    beta_matrix = [[0] * N for column in range(T)] #initialize beta-matrix 
    # Initialize beta for last time-step.
    for i in range(N):
        beta_matrix[T-1][i] = scalers[T-1] #Formula 2.26
    # Compute beta from t to T-1:
    for t in range(T-2, -1, -1):
        for i in range(N):
            beta_matrix[t][i] = sum(beta_matrix[t+1][j] * A[i][j] * B[j][T_sequence[t+1]] for j in range(N)) #Formula 2.30
        for i in range(N):
            beta_matrix[t][i] *= scalers[t] #scale values
    return beta_matrix
    
def calculate_gammas(A, B, alpha, beta_matrix, T_sequence):
    N = len(A)
    T = len(T_sequence)
    gamma = [[0] * N for _ in range(T)] #Formula 2.34 init
    di_gamma = [[[0] * N for _ in range(N)] for _ in range(T-1)] # formula 2.32 init

    for t in range(T-1):
        for i in range(N):
            for j in range(N):
                di_gamma[t][i][j] = alpha[t][i] * A[i][j] * B[j][T_sequence[t+1]] * beta_matrix[t+1][j]#2.32
            gamma[t][i] = sum(di_gamma[t][i][j] for j in range(N))#2.34
    for i in range(N):
        gamma[T-1][i] = alpha[T-1][i]

    return gamma, di_gamma

def estimate_lambda(A, B, pi, T_sequence): #2.40
    #2.39 below:
    alpha, scalers = alpha_pass(A, B, pi, T_sequence) 
    beta = beta_pass(A, B, T_sequence, scalers) 
    gamma, di_gamma = calculate_gammas(A, B, alpha, beta, T_sequence)

    N = len(A)
    M = len(B[0])
    # Re-estimate initial state distribution
    new_pi = [[gamma[0][i] for i in range(N)]] #2.37
    # Re-estimate transition probabilities
    new_A = [[0] * N for _ in range(N)] #init 2.35
    for i in range(N):
        for j in range(N):
            #2.35
            numerator = sum(di_gamma[t][i][j] for t in range(len(T_sequence) - 1))
            denominator = sum(gamma[t][i] for t in range(len(T_sequence) - 1))
            new_A[i][j] = numerator / denominator if denominator > 0 else 0
    # Re-estimate emission probabilities
    new_B = [[0] * M for _ in range(N)]
    for j in range(N):
        for k in range(M):#2.36
            numerator = sum(gamma[t][j] for t in range(len(T_sequence)) if T_sequence[t] == k)
            denominator = sum(gamma[t][j] for t in range(len(T_sequence)))
            new_B[j][k] = numerator / denominator if denominator > 0 else 0
    return new_A, new_B, new_pi


def baum_welch(A, B, pi, T_sequence, max_time=0.8):
    # Initial re-estimation of parameters
    updated_A, updated_emissions, updated_initial_state = estimate_lambda(
        A, B, pi, T_sequence
    )
    log_likelihood_previous = float("-inf")
    start_time = time.time()
    while True:
        # Update current parameters
        A, B, pi = (
            updated_A,
            updated_emissions,
            updated_initial_state,
        )
        _, scalers = alpha_pass(A, B, pi, T_sequence)
        log_likelihood_current = compute_log_likelihood(scalers)

        if log_likelihood_previous > log_likelihood_current or (time.time() - start_time) > max_time:
            break

        log_likelihood_previous = log_likelihood_current
        updated_A, updated_emissions, updated_initial_state = estimate_lambda(
            A, B, pi, T_sequence
        )
    return updated_A, updated_emissions

def compute_log_likelihood(scalers):
    return -sum(math.log(scaler) for scaler in scalers)

A_opt, B_opt = baum_welch(A, B, pi, T_sequence)

def format_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    elements = []
    for row in matrix:
        elements.extend([f"{value:.6g}" for value in row])
    return f"{rows} {cols} " + " ".join(map(str, elements)) + " "

print(format_matrix(A_opt))
print(format_matrix(B_opt))