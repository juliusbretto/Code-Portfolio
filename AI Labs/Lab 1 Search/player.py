#!/usr/bin/env python3
import time
import numpy as np
from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import math
import sys

def game_state_hashed(node):
    fish_coordinates = tuple(node.state.get_fish_positions().items())
    hook_coordinates = tuple(node.state.hook_positions.items())
    scores_players = tuple(node.state.player_scores.items())
    return hash((fish_coordinates,hook_coordinates,scores_players))

def calculate_distance(fish_position, hook_position):
    horizontal_distance = abs(fish_position[0] - hook_position[0])
    wrapped_distance = min(horizontal_distance, 20 - horizontal_distance)
    vertical_distance = abs(fish_position[1] - hook_position[1])
    return wrapped_distance + vertical_distance

def heuristic_evaluation(game_state):
    player_score_difference = game_state.state.player_scores[0] - game_state.state.player_scores[1]
    heuristic_value = 0
    
    for fish_key, fish_location in game_state.state.fish_positions.items():
        player_distance = calculate_distance(fish_location, game_state.state.hook_positions[0])
        opponent_distance = calculate_distance(fish_location, game_state.state.hook_positions[1])
        fish_score = game_state.state.fish_scores[fish_key]
        
        # Add penalty if opponent is closer to a high-value fish
        if opponent_distance < player_distance and fish_score > 0:
            heuristic_value -= fish_score / (1 + opponent_distance)

        # Reward moves where player can catch valuable fish
        if player_distance < opponent_distance:
            heuristic_value += fish_score / (1 + player_distance)
        
        # Is the hook directly at a fish position, meaning it can catch immediately?
        if player_distance == 0 and fish_score >0:
            return float("inf")
        heuristic_value = max(heuristic_value, fish_score*math.exp(-player_distance)) 

    return player_score_difference + heuristic_value


class PlayerControllerMinimax(PlayerController):
    def __init__(self):
        super().__init__()

    def player_loop(self):
        first_msg = self.receiver()
        while True:
            msg = self.receiver()
            node = Node(message=msg, player=0)
            best_move = self.search_best_next_move(node)
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        start_time = time.time()
        try:
            return ACTION_TO_STR[self.iterative_deepening_search(initial_tree_node, start_time)]
        except TimeoutError:
            return "stay"

    def alpha_beta_pruning(self, current_node, max_depth, lower_bound, upper_bound, current_player, start_time, memo):
        node_hash = game_state_hashed(current_node)

        # Check if the state is already cached and can be reused
        if node_hash in memo and memo[node_hash][0] >= max_depth:
            return memo[node_hash][1]
        # Generate children and sort them based on heuristic evaluation
        possible_moves = current_node.compute_and_get_children()
        possible_moves.sort(key=heuristic_evaluation, reverse=(current_player == 0))

        
        prune_threshold = 7  # Limit number of branches to explore
        possible_moves = possible_moves[:prune_threshold]
        
        if time.time() - start_time >= 0.05:
            raise TimeoutError
        if max_depth == 0 or not possible_moves:
            evaluation_score = heuristic_evaluation(current_node)
        elif current_player == 0:
            # Maximizing player, green boat
            evaluation_score = float("-inf")
            for next_node in possible_moves:
                evaluation_score = max(
                    evaluation_score,
                    self.alpha_beta_pruning(next_node, max_depth - 1, lower_bound, upper_bound, 1, start_time, memo)
                )
                lower_bound = max(lower_bound, evaluation_score) #lower_bound = alpha
                if lower_bound >= upper_bound:
                    break
        else:
            # Minimizing player, red boat
            evaluation_score = float("inf")
            for next_node in possible_moves:
                evaluation_score = min(
                    evaluation_score,
                    self.alpha_beta_pruning(next_node, max_depth - 1, lower_bound, upper_bound, 0, start_time, memo)
                )
                upper_bound = min(upper_bound, evaluation_score) #upper_bound = beta
                if lower_bound >= upper_bound:
                    break

        memo[node_hash] = (max_depth, evaluation_score)
        return evaluation_score

    def iterative_deepening_search(self, root_node, start_time):
        search_depth = 1
        optimal_move = None
        memoization = {}
        
        while True:
            try:
               
                potential_moves = root_node.compute_and_get_children()
                move_scores = []
                
                #Initialization
                for potential_move in potential_moves:
                    score = self.alpha_beta_pruning(
                        potential_move,
                        search_depth,
                        float("-inf"),
                        float("inf"),
                        1, 
                        start_time,
                        memoization
                    )
                    move_scores.append(score)
                
                highest_score_index = move_scores.index(max(move_scores))
                optimal_move = potential_moves[highest_score_index].move

                search_depth += 1
            except TimeoutError:
                break
        
        return optimal_move

"""
TO RUN THE PROGRAM:
python3.7 -m venv fishingderby
source fishingderby/bin/activate
python main.py settings.yml
"""