

def parse_matrix(input_line):
    """Parse a single input line into a matrix."""
    elements = input_line.split()
    rows = int(elements.pop(0))
    cols = int(elements.pop(0))
    return [[float(elements.pop(0)) for _ in range(cols)] for _ in range(rows)]


def parse_observation(input_line):
    """Parse the observation sequence from input."""
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


def viterbi_algorithm(transitions, emissions, initial_state, observations):
       N = len(transitions)
    T = len(observations)

    # Initialize viterbi and back_ptr-matrices
    v = [[0 for _ in range(N)] for _ in range(T)]
    back_ptr = [[0 for _ in range(N)] for _ in range(T)]

    # Initialize v[0][states]:
    for state in range(N):
        v[0][state] = initial_state[0][state] * emissions[state][observations[0]]

    # Iteratively fill viterbi and back-pointer matrices
    for t in range(1, T):
        for curr_state in range(N):
            max_prob = -1
            max_idx = -1
            for prev_state in range(N):
                prob = v[t-1][prev_state] * transitions[prev_state][curr_state]
                if prob > max_prob:
                    max_prob = prob
                    max_idx = prev_state
            v[t][curr_state] = max_prob * emissions[curr_state][observations[t]]
            back_ptr[t][curr_state] = max_idx

    # Backtrack to find the most likely state sequence
    most_likely_sequence = [0] * T
    most_likely_sequence[T-1] = max(range(N), key=lambda state: v[T-1][state])
    for t in range(T-2, -1, -1):
        most_likely_sequence[t] = back_ptr[t+1][most_likely_sequence[t+1]]

    return most_likely_sequence


def main():
    # Read the input data
    transitions, emissions, initial_state, observations = read_model_input()

    # Compute the most likely state sequence using Viterbi
    most_likely_sequence = viterbi_algorithm(transitions, emissions, initial_state, observations)

    # Output the result
    print(" ".join(map(str, most_likely_sequence)))


if __name__ == "__main__":
    main()
