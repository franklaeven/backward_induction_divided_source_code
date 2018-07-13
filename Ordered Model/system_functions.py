from states import State
from states import RoundState
from space_functions import transition_state
import numpy as np

def count_probabilities3(state_space,ordering_space,action_space):
    counter = 0
    for s in state_space:
            for ordering in ordering_space:
                player1 = ordering[0]
                player2 = ordering[1]
                player3 = ordering[2]
                for action1 in action_space[RoundState(s,player1)]:
                    s1 = transition_state(s,action1,player1)
                    for action2 in action_space[RoundState(s1,player2)]:
                        s2 = transition_state(s1,action2,player2)
                        for action3 in action_space[RoundState(s2,player3)]:
                            counter+=1
    return counter

def count_probabilities2(state_space,ordering_space,action_space):
    counter = 0
    for s in state_space:
            for ordering in ordering_space:
                player1 = ordering[0]
                player2 = ordering[1]
                for action1 in action_space[RoundState(s,player1)]:
                    s1 = transition_state(s,action1,player1)
                    for action2 in action_space[RoundState(s1,player2)]:
                        counter+=1
    return counter

def count_probabilities1(state_space,ordering_space,action_space):
    counter = 0
    for s in state_space:
            for ordering in ordering_space:
                player1 = ordering[0]
                for action1 in action_space[RoundState(s,player1)]:
                    counter+=1
    return counter

def quantile_response(action_nodes,value_function,utility_function,rationality_constant = 3):
    utility_vector = list()
    node_depth = action_nodes[0].node_depth
    current_player = action_nodes[0].ordering[node_depth-2]
    
    for node in action_nodes:
        value_action = value_function[node][current_player]
        utility_vector.append(utility_function(value_action))
    
    max_utility = np.max(utility_vector)
    utility_vector_diminished = utility_vector - max_utility
    
    quantile_responses_non_normalized = np.exp(rationality_constant*utility_vector_diminished)*np.exp(rationality_constant*max_utility)
    
    quantile_responses = quantile_responses_non_normalized/np.sum(quantile_responses_non_normalized)
    return quantile_responses
        
    
def simple_utility_function(value):
    return value