import constants

import numpy as np

from space_functions import populate_state_space 
from states import State
from nodes import Node

def calculate_matrix_product(t, probability_matrices):
    matrix_product_time_t = probability_matrices[0]
    
    for t in range(1,t):
        matrix_product_time_t = np.dot(matrix_product_time_t,probability_matrices[t])
        
    return matrix_product_time_t

def calculate_probability_consensus(t, probability_matrices, begin_state):
    probability_matrix_time_t = calculate_matrix_product(t, probability_matrices)
    probability_consensus = np.sum(probability_matrix_time_t[begin_state,list(constants.CONSENSUS_STATES)])    
    return probability_consensus
	
def calculate_expected_value_t(t, value_functions, begin_state):
	n = Node(begin_state,None,(None,None,None))
	return value_functions[t][n]

def get_probability_data(probability_matrices, begin_state_index = 0):
    x_data = [np.round(t*constants.TIME_STEP,2) for t in range(constants.TOTAL_TIME+1)]
    y_data = [calculate_probability_consensus(t, probability_matrices, begin_state_index) for t in range(constants.TOTAL_TIME+1)]
    
    x_label = "Time(s)"
    y_label = "Probablity"
    
    legend_labels = ["Player 1","Player 2","Player 3"]
    
    plot_title = "Probability that a consensus has been reached."
    
    return x_data, y_data, x_label, y_label, legend_labels, plot_title 
    
def get_value_data(value_functions, begin_state_index = 0):
    state_space = populate_state_space()
    begin_state = state_space[begin_state_index]   
    x_data = [np.round(t*constants.TIME_STEP,2) for t in range(constants.TOTAL_TIME+1)]
    y_data = [calculate_expected_value_t(t, value_functions, begin_state) for t in range(constants.TOTAL_TIME+1)]
    
    x_label = "Time(s)"
    y_label = "Value (proportion of initial pot t=0)"
    
    legend_labels = ["Player 1","Player 2","Player 3"]
    
    plot_title = "Expected value of each player as a proportion of the initial pot."
    
    return x_data, y_data, x_label, y_label, legend_labels, plot_title