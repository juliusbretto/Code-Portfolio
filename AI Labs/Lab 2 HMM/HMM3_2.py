import sys

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
