import constants
import numpy as np
from nodes import Node

# Value functions and probability functions

def calculate_value_function_turn3(node_tree, t, value_function_turn_t1):
    value_function_turn3 = dict()
    #Loop through nodes at current depth in the node tree
    for node in node_tree[constants.A3_NODE_DEPTH]:
        # Create parent node
        parent_node = Node(node.end_state,None,(None,None,None))
        # Check if consensus is reach, if so all possible future value is (0,0,0) since the game is over. 
        # Else return value of being in current end state at t+1
        value_t1 = np.zeros(constants.N_PLAYERS) if node.end_state.is_consensus else value_function_turn_t1[parent_node]
        # Payoff function for current end node at time t
        payoff = np.zeros(constants.N_PLAYERS) if node.begin_state.is_consensus else payoff_function(node,t)
        value_function_turn3[node] = value_t1+payoff
    return value_function_turn3

def calculate_probability_dictionary_turn3(node_tree, value_function_turn3, utility_functions):
    
    probability_dictionary = dict()
    # Loop through parents of the previous depth in the node tree
    for parent in node_tree[constants.A2_NODE_DEPTH]:
        # Gets the sibling nodes from the parent node
        sibling_nodes = parent.children
        # Calculate the quantal responses of the third turn player
        qantal_responses = calculate_quantal_response(sibling_nodes,value_function_turn3,utility_functions)
        for i in range(len(sibling_nodes)):
            probability_dictionary[sibling_nodes[i]] = qantal_responses[i]                  
    return probability_dictionary

def calculate_value_function_turn2(node_tree, value_function_turn3, probability_turn3):
    value_function_turn2 = dict()
    # Loop through nodes at the current depth of the node tree
    for node in node_tree[constants.A2_NODE_DEPTH]:
        expected_value = 0
        # Calculate the expected value of the second turn node
        for child in node.children:
            expected_value += probability_turn3[child]*value_function_turn3[child]
        
        value_function_turn2[node] = expected_value
    return value_function_turn2

def calculate_probability_dictionary_turn2(node_tree,value_function_turn2,utility_functions):
    probability_dictionary = dict()
    for parent in node_tree[constants.A1_NODE_DEPTH]:
        sibling_nodes = parent.children
        qantal_responses = calculate_quantal_response(sibling_nodes,value_function_turn2,utility_functions)
        for i in range(len(sibling_nodes)):
            probability_dictionary[sibling_nodes[i]] = qantal_responses[i]  
    return probability_dictionary   

def calculate_value_function_turn1(node_tree, value_function_turn2, probability_turn2):
    value_function_turn1 = dict()
    for node in node_tree[constants.A1_NODE_DEPTH]:
        expected_value = 0
        for child in node.children:
            expected_value += probability_turn2[child]*value_function_turn2[child]
        
        value_function_turn1[node] = expected_value
    return value_function_turn1

def calculate_probability_dictionary_turn1(node_tree,value_function_turn1,utility_functions):
    probability_dictionary = dict()
    
    sibling_nodes = node_tree[constants.A1_NODE_DEPTH]
    qantal_responses = calculate_quantal_response(sibling_nodes,value_function_turn1,utility_functions)
    
    for i in range(len(sibling_nodes)):
        probability_dictionary[sibling_nodes[i]] = qantal_responses[i]  
        
    return probability_dictionary

def calculate_value_ordering(value_function_turn1, probability_dictionary_turn1):
    value = np.zeros(constants.N_PLAYERS)
    
    value_function_turn1_values = list(value_function_turn1.values())
    probability_dictionary_turn1_values = list(probability_dictionary_turn1.values())
    
    for i, value_turn1 in enumerate(value_function_turn1_values):
        value += value_turn1*probability_dictionary_turn1_values[i]
    return value

def calculate_value_function_turn_state(value_function_ordering, probability_dictionary_ordering):
    value = np.zeros(constants.N_PLAYERS)
    
    value_function_ordering_values = list(value_function_ordering.values())
    probability_dictionary_ordering_values = list(probability_dictionary_ordering.values())
    
    for i, value_turn_ordering in enumerate(value_function_ordering_values):
        value += value_turn_ordering*probability_dictionary_ordering_values[i]
    return value  

# Function that determines probability of player ordering
    
def calculate_probability_ordering(ordering):
    
    probability_player1_first = constants.RECOGNITION_PROBABILITIES[ordering[0]]
    probability_player2_first = constants.RECOGNITION_PROBABILITIES[ordering[1]]
    probability_player3_first = constants.RECOGNITION_PROBABILITIES[ordering[2]]
    
    probability_of_ordering = (probability_player1_first*probability_player2_first)/              \
                              (probability_player2_first+probability_player3_first)
    
    return probability_of_ordering         

# Payoff function and quantal response

def calculate_quantal_response(sibling_nodes,value_function,utility_functions,
                               rationality_constant = constants.RATIONALITY_CONSTANT):
    utility_vector = list()
    # Calculates the node depth
    node_depth = sibling_nodes[0].node_depth
    # Check who the current player is                         
    current_player = sibling_nodes[0].ordering[node_depth]
    #Loops over all sibling nodes and gets the utility of each node for the current player
    for node in sibling_nodes:
        value_action = value_function[node]
        utility_function = utility_functions[current_player]
        utility_vector.append(utility_function(value_action,current_player))
    #Find the highest utility and subtracts it from the utility vector for computational reasons
    max_utility = np.max(utility_vector)
    utility_vector_diminished = utility_vector - max_utility
    #Calculates non normalized quantal responses of current player
    quantal_responses_non_normalized = np.exp(rationality_constant*utility_vector_diminished)
    #Normalizes the quantal responses
    quantal_responses = quantal_responses_non_normalized/np.sum(quantal_responses_non_normalized)
    return quantal_responses

def payoff_function(node,t):
    assert type(node) == Node
    decayed_payoff = np.zeros(constants.N_PLAYERS)
    
    if node.end_state.is_consensus:
        non_decayed_payoff = np.array([constants.PAYOFF_DICTIONARY[claim] for claim in node.end_state.state_content])
        decayed_payoff = non_decayed_payoff*decay_function(t)
    return decayed_payoff

def decay_function(t):
    return 1-t/constants.TOTAL_TIME