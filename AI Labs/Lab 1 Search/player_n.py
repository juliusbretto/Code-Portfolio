#!/usr/bin/env python3
#python main.py settings.yml
import time
import numpy as np
from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import sys
import math

#Function that gives unique hash to game state. Makes it possible to skip evaluation of this game state if already calculated.
def game_state_hashed(node):
    fish_coordinates = tuple(node.state.get_fish_positions().items()) #get all fish positions (their coordinates) for current game state
    hook_coordinates = tuple(node.state.hook_positions.items()) #get hook positions of both players for current game state.
    scores_players = tuple(node.state.player_scores.items()) #Get current players scores for game state.
    return hash((fish_coordinates,hook_coordinates,scores_players)) #Give current game state a unique hash value.

#Dist between hook and fish
def calculate_distance(fish_position, hook_position): #Input: coordinates of a fish and a hook
    horizontal_distance = abs(fish_position[0] - hook_position[0]) #Absolute difference in x-coordinates
    #Adjusts for the fact that the grid wraps around horisontally:
    #Use the smallest difference between wrapped around distance and direct distance:
    wrapped_distance = min(horizontal_distance, 20 - horizontal_distance)
    vertical_distance = abs(fish_position[1] - hook_position[1]) #Absolute distance y-coordinates.
    return wrapped_distance + vertical_distance #Manhattan distance (because movement only possible in x and y directions).

#Calculates heuristic value for a given game state
#We (player 0) always want to maximize this heuristic value.
#
def heuristic_evaluation(game_state): #game state = players scores, fish positions and their values, hook positions
    #Heuristic based on:
    #Difference in player scores 
    #Fishes positions and values
    #How close are the players to the fishes

    #Calculate player score difference between player 0 and 1.
    #If player 0 has higher score the player score difference will be positive, resulting in a higher returned heuristic value for that game state
    #If player 1 has higher score, the player score differnece will be negative, resulting in a lower returned heuristic value.
    player_score_difference = game_state.state.player_scores[0] - game_state.state.player_scores[1]
    heuristic_value = 0 #Init
    
    for fish_key, fish_location in game_state.state.fish_positions.items(): #Loop through uncaught unique fish-keys and their respective position.
        player_distance = calculate_distance(fish_location, game_state.state.hook_positions[0]) #how far is player 0 i from current fish? (0an indikerar på player 0)
        opponent_distance = calculate_distance(fish_location, game_state.state.hook_positions[1]) #How far away is player 1 from current fish? (1an indikerar på player 1)
        fish_score = game_state.state.fish_scores[fish_key] #How many points does the fish give (or take if negative) if fished?
        
        
        if player_distance == 0 and fish_score >0:
            return float("inf") #Return infiity high heuristic score
        if opponent_distance == 0 and fish_score >0:
            return -float("inf") #Return infiity low heuristic score
     
        # Add penalty if opponent is closer to a positive-value fish:
        if opponent_distance < player_distance and fish_score > 0:
            heuristic_value -= fish_score / (1 + opponent_distance)#penalty propositional to fish score and oponents distance to fish

        # Reward moves where player can catch valuable fish
        if player_distance < opponent_distance and fish_score > 0:
            heuristic_value += fish_score / (1 + player_distance) #Opposite to above
        
        if fish_score > 5: #For more valuable fish types:
            #Below code uses (the high) fish score as weight and uses exponential distance so that the weight is more sensitive.
            #Very close to the fish is rewarded significantly more than being moderately close.
            heuristic_value +=  fish_score * (math.exp(-player_distance) - math.exp(-opponent_distance))
        
    #Add player_score_diffence to heuristic score
    return heuristic_value + player_score_difference #How favorable is the game state for player 0?


class PlayerControllerMinimax(PlayerController):
    def __init__(self):
        super().__init__()

    def player_loop(self): #Main loop  where the AI interacts with the game:
        first_msg = self.receiver()
        while True: #Continuously process game updates and and determines next move
            msg = self.receiver() #Ai recieves current game state as msg from game engine
            node = Node(message=msg, player=0) #Get game state for player 0 based on message (Root node)
            best_move = self.search_best_next_move(node) #predicts best next move based on game state
            self.sender({"action": best_move, "search_time": None}) #Sends best move to game engine to continue the game

    #Function that starts timer and calls the iterative deepning search and returns best move for player 0
    def search_best_next_move(self, initial_tree_node):
        start_time = time.time()
        try:
            return ACTION_TO_STR[self.iterative_deepening_search(initial_tree_node, start_time)]
        except TimeoutError:
            return "stay"
        
    #MinMax-algo with pruning
    #Pupose:
    #Explores game tree to find best possible move for current player. 
    #Skippes irrelevant branches with alpha-beta-pruning.
    """
    Params:
        current_node: The current game state node being evaluated.
        max_depth: The remaining depth of the search (how far to look ahead).
        alpha: The best value the maximizing player (Player 0) is guaranteed so far.
        beta: The best value the minimizing player (Player 1) is guaranteed so far.
        current_player: Indicates whether it's Player 0's turn (maximizing) or Player 1's turn (minimizing).
        start_time: The start time of the search, used to check time limits.
        memo: A dictionary to store heuristic evaluations of previously visited game states for efficiency.
    """
    
    def alpha_beta_pruning(self, current_node, max_depth, alpha, beta, current_player, start_time, memo):
        node_hash = game_state_hashed(current_node)  #Hash current node (game state) to check if already been evaluated

        #If the current state has already been evaluated at an equal or greater depth, return the stored heuristic value.
        if node_hash in memo and memo[node_hash][0] >= max_depth:
            return memo[node_hash][1] #Return memorized heurstic
        # Generate children and sort them based on heuristic evaluation
        possible_moves = current_node.compute_and_get_children() #Compute and get states for children nodes
        possible_moves.sort(key=heuristic_evaluation, reverse=(current_player == 0)) #Sort nodes (för pruning algo) based on which players turn it is. Improves pruning by evaluating the most promising branches first.
       
        if time.time() - start_time >= 0.04: #End iterative deepning search when time is up to return best move
            raise TimeoutError
        if max_depth == 0 or not possible_moves: #End of tree (Accordinng to max depth chosen) or no more possible moves.
            evaluation_score = heuristic_evaluation(current_node) #Calculate evaluation score for state in end of tree
        elif current_player == 0: #If our player and we are not at the bottom of the tree:
            # Maximizing player
            evaluation_score = float("-inf") #Init
            for next_node in possible_moves: #Loop through children nodes
                evaluation_score = max( #Return max evaluation between its children
                    evaluation_score,
                    self.alpha_beta_pruning(next_node, max_depth - 1, alpha, beta, 1, start_time, memo)
                )
                #Tree pruning
                alpha = max(alpha, evaluation_score) 
                if alpha >= beta:
                    break
        else:
            # Minimizing player
            evaluation_score = float("inf")
            for next_node in possible_moves:
                evaluation_score = min( #Return min evaluation between children states.
                    evaluation_score,
                    self.alpha_beta_pruning(next_node, max_depth - 1, alpha, beta, 0, start_time, memo)
                )
                beta = min(beta, evaluation_score)
                if alpha >= beta:
                    break

        memo[node_hash] = (max_depth, evaluation_score)
        return evaluation_score

    #Algo that ensures that we traverse one tree depth at a time for all children nodes within the given time.
    #Purpose:
    #Gradually increasing the search depth (iterative deepening).
    #Using alpha-beta pruning to efficiently evaluate game states at each depth.
    #Returning the best move found before the time limit is reached.

    #Guarentees a move within the time limit compared to regular minimax:
    #When time limit is reached, algo returns the best move found at deepest completed level even if deeper searches are interrupted.
    #Regular minimax searches directly to a fixed depth with DFS and amy not return a move within time limit.
    #In high complex games (example with 5 possible moves) the number of nodes to evaluate increases exponantielly with depth: 5^2, 5^3 etc.

    def iterative_deepening_search(self, root_node, start_time):
        search_depth = 1 #Init tree deph
        optimal_move = None #The move we want to return for player 0
        memoization = {} #Init our memo
        
        while True: #Loop down tree until time out.
            try:
               
                potential_moves = root_node.compute_and_get_children() #Compute and get children nodes (game states for possibles moves)
                move_scores = [] #Evaluations cores for possible moves (childs)
                
                for potential_move in potential_moves: #Alphabeta pruning for every possible node.
                    score = self.alpha_beta_pruning( #Return score for current next move with minmax-algo
                        potential_move, #Current move
                        search_depth, #Current search depht
                        float("-inf"), #init alpha
                        float("inf"), #init beta
                        1, #Next turn is opponent player
                        start_time,
                        memoization
                    )
                    move_scores.append(score) #Append score for current move (child).
                
                highest_score_index = move_scores.index(max(move_scores)) #Which move ended up with highest score with minmax? (index)
                optimal_move = potential_moves[highest_score_index].move #return move corresponidng to highest score for the current tree-depth.

                search_depth += 1 #add tree depth as long as we have time left.
            except TimeoutError:
                break
        
        return optimal_move

"""
TO RUN THE PROGRAM:
python3.7 -m venv fishingderby
source fishingderby/bin/activate
python main.py settings.yml
"""