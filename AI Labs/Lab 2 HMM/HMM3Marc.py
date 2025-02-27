import math
import time

def parse_matrix(input_line):
    elements = input_line.split()
    rows = int(elements.pop(0))
    cols = int(elements.pop(0))
    return [[float(elements.pop(0)) for _ in range(cols)] for _ in range(rows)]

def parse_observation(input_line):
    elements = input_line.split()
    return [int(x) for x in elements[1:]]


def read_model_input():
    inputs = []
    while True:
        try:
            inputs.append(input())
        except EOFError:
            break
    transition_matrix = parse_matrix(inputs[0])
    emission_matrix = parse_matrix(inputs[1])
    initial_distribution = parse_matrix(inputs[2])
    observation_sequence = parse_observation(inputs[3])
    return transition_matrix, emission_matrix, initial_distribution, observation_sequence


def format_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    elements = []
    for row in matrix:
        elements.extend(row)
    return f"{rows} {cols} " + " ".join(map(str, elements)) + " "

"""
Similiar to forward-algo, but calculates the prob to observe all future
observations t+1:T given current state instead of calculating the prob to have had observed the sequence
of observations 1:t given current state. We use formula 2.30 instead of 2.13 where we sum over
future states instead of previous states.
"""
def calculate_beta(A, B, obs, scalers):
    N = len(A)
    T = len(obs)
    beta_matrix = [[0] * N for column in range(T)] #initialize beta-matrix 
    # Initialize beta for last time-step.
    for i in range(N):
        beta_matrix[T-1][i] = scalers[T-1] #Formula 2.26
    # Compute beta from t to T-1:
    for t in range(T-2, -1, -1):
        for i in range(N):
            beta_matrix[t][i] = sum(beta_matrix[t+1][j] * A[i][j] * B[j][obs[t+1]] for j in range(N)) #Formula 2.30
        for i in range(N):
            beta_matrix[t][i] *= scalers[t] #scale values
    return beta_matrix

#Reuse forward_algo from HMM1 but implement scaler.
def calculate_alpha(transitions, emissions, initial_state, observations):
    N = len(transitions)
    T = len(observations)

    # Initialize alpha with the first observation
    alpha = []
    alpha_t0 = []
    for state in range(N):
        alpha_t0.append(initial_state[0][state] * emissions[state][observations[0]])
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
                sum_prob += alpha[t-1][prev_state] * transitions[prev_state][curr_state]
            alpha_t.append(sum_prob * emissions[curr_state][observations[t]])
        # Normalize the current alpha_t
        scaler_t = 1 / sum(alpha_t)
        alpha_t = [value * scaler_t for value in alpha_t]
        alpha.append(alpha_t)
        scalers.append(scaler_t)

    return alpha, scalers


# Gamma 
def calculate_gammas(A, B, alpha, beta_matrix, obs):
    N = len(A)
    T = len(obs)
    gamma = [[0] * N for _ in range(T)] #Formula 2.34 init
    di_gamma = [[[0] * N for _ in range(N)] for _ in range(T-1)] # formula 2.32 init

    for t in range(T-1):
        for i in range(N):
            for j in range(N):
                di_gamma[t][i][j] = alpha[t][i] * A[i][j] * B[j][obs[t+1]] * beta_matrix[t+1][j]#2.32
            gamma[t][i] = sum(di_gamma[t][i][j] for j in range(N))#2.34
    for i in range(N):
        gamma[T-1][i] = alpha[T-1][i]

    return gamma, di_gamma


def reestimate_parameters(A, B, pi, obs): #2.40
    #2.39 below:
    alpha, scalers = calculate_alpha(A, B, pi, obs) 
    beta = calculate_beta(A, B, obs, scalers) 
    gamma, di_gamma = calculate_gammas(A, B, alpha, beta, obs)

    N = len(A)
    M = len(B[0])
    # Re-estimate initial state distribution
    new_pi = [[gamma[0][i] for i in range(N)]] #2.37
    # Re-estimate transition probabilities
    new_A = [[0] * N for _ in range(N)] #init 2.35
    for i in range(N):
        for j in range(N):
            #2.35
            numerator = sum(di_gamma[t][i][j] for t in range(len(obs) - 1))
            denominator = sum(gamma[t][i] for t in range(len(obs) - 1))
            new_A[i][j] = numerator / denominator if denominator > 0 else 0
    # Re-estimate emission probabilities
    new_B = [[0] * M for _ in range(N)]
    for j in range(N):
        for k in range(M):#2.36
            numerator = sum(gamma[t][j] for t in range(len(obs)) if obs[t] == k)
            denominator = sum(gamma[t][j] for t in range(len(obs)))
            new_B[j][k] = numerator / denominator if denominator > 0 else 0
    return new_A, new_B, new_pi

def compute_log_likelihood(scalers):
    return -sum(math.log(scaler) for scaler in scalers)


def baum_welch(transition_matrix, emission_matrix, initial_state, observations, max_time=0.8):
    # Initial re-estimation of parameters
    updated_transitions, updated_emissions, updated_initial_state = reestimate_parameters(
        transition_matrix, emission_matrix, initial_state, observations
    )
    log_likelihood_previous = float("-inf")
    start_time = time.time()
    while True:
        # Update current parameters
        transition_matrix, emission_matrix, initial_state = (
            updated_transitions,
            updated_emissions,
            updated_initial_state,
        )
        _, scalers = calculate_alpha(transition_matrix, emission_matrix, initial_state, observations)
        log_likelihood_current = compute_log_likelihood(scalers)

        if log_likelihood_previous > log_likelihood_current or (time.time() - start_time) > max_time:
            break

        log_likelihood_previous = log_likelihood_current
        updated_transitions, updated_emissions, updated_initial_state = reestimate_parameters(
            transition_matrix, emission_matrix, initial_state, observations
        )
    return updated_transitions, updated_emissions


def main():
    A_matrix, B_matrix, pi, observations= read_model_input()
    A_matrix_new, B_matrix_new = baum_welch(A_matrix, B_matrix, pi, observations)

    print(format_matrix(A_matrix_new))
    print(format_matrix(B_matrix_new))

if __name__ == "__main__":
    main()
