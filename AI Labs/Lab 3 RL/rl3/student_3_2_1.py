#!/usr/bin/env python3
# rewards: [golden_fish, jellyfish_1, jellyfish_2, ... , step]
rewards = [-10, -10, -10, -10, 10, -10, -10, -10, 10, -10, -10, -10, -10, 15]
#rewards = [-10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, 15]

#Never catching any fish
#Moderate learning, high discounting (low might be better)

# Q learning learning rate
alpha = 0.5

# Q learning discount rate
gamma = 0.9

# Epsilon initial
epsilon_initial = 1

# Epsilon final
epsilon_final = 1

# Annealing timesteps
annealing_timesteps = 1

# threshold
threshold = 1e-6
