#!/usr/bin/env python3
#python main.py < sequences.json

from player_controller_hmm import PlayerControllerHMMAbstract
from constants import *
import random
import math
import time
import sys
import numpy as np

EPSILON = sys.float_info.epsilon  # avoid division by zero


def calculate_alpha(transitions, emissions, initial_state, observations):
    N = len(transitions)
    T = len(observations)

    # Initialize alpha with the first observation
    alpha = []
    alpha_t0 = []
    for state in range(N):
        alpha_t0.append(initial_state[0][state] * emissions[state][observations[0]])
    # Normalize the first step
    scaler_0 = 1 / (sum(alpha_t0) + EPSILON)  # Add epsilon to avoid division by zero
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
        scaler_t = 1 / (sum(alpha_t) + EPSILON)  # Add epsilon to avoid division by zero
        alpha_t = [value * scaler_t for value in alpha_t]
        alpha.append(alpha_t)
        scalers.append(scaler_t)

    return alpha, scalers

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

def baum_welch(A, B, PI, observations, max_iter=10):
    for _ in range(max_iter):
        alpha, scalers = calculate_alpha(A, B, PI, observations)
        beta = calculate_beta(A, B, observations, scalers)
        gamma, di_gamma = calculate_gammas(A, B, alpha, beta, observations)

        # Re-estimate PI
        for i in range(len(PI[0])):
            PI[0][i] = gamma[0][i]

        # Re-estimate A
        for i in range(len(A)):
            for j in range(len(A[i])):
                numerator = sum(di_gamma[t][i][j] for t in range(len(observations) - 1))
                denominator = sum(gamma[t][i] for t in range(len(observations) - 1))
                A[i][j] = numerator / (denominator + EPSILON)

        # Re-estimate B
        for i in range(len(B)):
            for k in range(len(B[i])):
                numerator = sum(gamma[t][i] for t in range(len(observations)) if observations[t] == k)
                denominator = sum(gamma[t][i] for t in range(len(observations)))
                B[i][k] = numerator / (denominator + EPSILON)

    return A, B, PI

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


def initialize_fish_model(n_states, n_emissions): #Function that init our model parameters with normalized values.
    A = np.random.rand(n_states, n_states)
    A /= A.sum(axis=1, keepdims=True) 
    B = np.random.rand(n_states, n_emissions)
    B /= B.sum(axis=1, keepdims=True)
    PI = np.random.rand(1, n_states)
    PI /= PI.sum()  
    return A, B, PI

class PlayerControllerHMM(PlayerControllerHMMAbstract):
    def init_parameters(self):
        self.HMM_models = [initialize_fish_model(1, N_EMISSIONS) for _ in range(N_SPECIES)] #List containing our fisg models we want to update with baum welch
        self.fish_observations = [[] for _ in range(N_FISH)]
        self.tested_fish = [False for _ in range(N_FISH)]

    def guess(self, time_step, fish_observations):
        for fish_model in range(N_FISH): 
            if self.tested_fish[fish_model] == False: #Only add  None-tested fishes.
                self.fish_observations[fish_model].append(fish_observations[fish_model])
        if time_step < 100: #Dont make guesses before time_step 100.  Balance between triaining (when to start guessing) and how many guess iterations we use.
            return None

        random_fish_ID = random.choice([fish for fish in range(N_FISH) if self.tested_fish[fish]==False]) #choose random fish if not tested already
        highest_probability = -float('inf')  # Init
        fish_type = None # init

        for fish_model, (A, B, pi) in enumerate(self.HMM_models): #Loop through all fish models
            _, alpha_probs = calculate_alpha(A, B, pi, self.fish_observations[random_fish_ID]) #Get alpha probs
            probabilities = -sum(math.log(scaler) for scaler in alpha_probs)  # log-likelihood
            if probabilities > highest_probability:  # Want to find highest prob model for the random selected fish
                highest_probability = probabilities
                fish_type = fish_model #Return guessed fish_model för selected fish
        
        self.tested_fish[random_fish_ID] = True #Marks the fish as tested

        return random_fish_ID, fish_type #Return the random fish we choosed and its corresponding model-guess.


    def reveal(self, correct, fish_id, true_type): #Handles the guess of incorrect fish from guess-function

        if correct==False: #If we guessed the wrong fish:
            A, B, pi = self.HMM_models[true_type] #Get model parameters of the fish we should have guessed on (these parameters need to get better)
            fish_observations = self.fish_observations[fish_id] #Get observations from the wrongly guessed fish
            self.HMM_models[true_type] = baum_welch(A, B, pi, fish_observations) #refine parameters of wrongly selected fish with Baum Welch iterative aproach.

#python main.py < sequences.json