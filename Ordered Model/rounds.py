import constants
import numpy as np

from nodes import Node

from states import State
from states import TurnState

from space_functions import get_state_index_dictionary

from simulation_functions import calculate_value_function_turn1
from simulation_functions import calculate_value_function_turn2
from simulation_functions import calculate_value_function_turn3

from simulation_functions import calculate_probability_dictionary_turn1
from simulation_functions import calculate_probability_dictionary_turn2
from simulation_functions import calculate_probability_dictionary_turn3

from simulation_functions import calculate_value_ordering
from simulation_functions import calculate_probability_ordering

from simulation_functions import calculate_value_function_turn_state

class Round:
    def __init__(self, t, state_space, action_space, value_function_tp1, utility_functions):
        self.t = t
        self.state_space = state_space
        self.action_space = action_space
        self.value_function_tp1 = value_function_tp1
        self.utility_functions = utility_functions
        self.value_function_t = None
        self.state_dictionary = get_state_index_dictionary(state_space)
        size_state_space = len(state_space)
        self.probability_matrix = np.zeros((size_state_space, size_state_space))
        
    def calculate_round(self):
        probability_dictionary_ordering = {ordering:calculate_probability_ordering(ordering) for ordering in constants.ORDERING_SPACE}
        value_function_state_t = dict()
        
        for state in self.state_space:
            value_function_ordering = dict()
            
            state_node = Node(state,None,(None,None,None))
            value_function_state_t[state_node] = 0
            
            for ordering in constants.ORDERING_SPACE:
                node_tree = self.generate_node_tree(state,ordering)
                
                ordering_node = Node(state, ordering, (None,None,None))
        
                value_function_turn3, probability_dictionary_turn3 = self.calculate_turn_3(node_tree)
                
                value_function_turn2, probability_dictionary_turn2 = self.calculate_turn_2(node_tree, value_function_turn3, 
                                                                                           probability_dictionary_turn3)
                
                value_function_turn1, probability_dictionary_turn1 = self.calculate_turn_1(node_tree, value_function_turn2, 
                                                                                           probability_dictionary_turn2)
                
                # Calculate expected value for every ordering and store it in a dictionary
                value_function_ordering[ordering_node] = calculate_value_ordering(value_function_turn1, probability_dictionary_turn1)                
                
                self.calculate_probability_matrix(probability_dictionary_turn3, probability_dictionary_turn2, 
                                     probability_dictionary_turn1, probability_dictionary_ordering, state, ordering)
                
            value_function_state_t[state_node] = calculate_value_function_turn_state(value_function_ordering, probability_dictionary_ordering)
            
        self.value_function_t = value_function_state_t
        
    def calculate_probability_matrix(self,probability_dictionary_turn3, probability_dictionary_turn2, 
                                     probability_dictionary_turn1, probability_dictionary_ordering, state, ordering):
        
        node_tree = self.generate_node_tree(state,ordering)
        
        for node in node_tree[constants.A3_NODE_DEPTH]:
            row_state_index = self.state_dictionary[state]
            col_state_index = self.state_dictionary[node.end_state]
            
            self.probability_matrix[row_state_index,col_state_index] += probability_dictionary_ordering[ordering]*     \
                                                                        probability_dictionary_turn1[node.parent.parent]*    \
                                                                        probability_dictionary_turn2[node.parent]*    \
                                                                        probability_dictionary_turn3[node]
                    
                    
                    
                            
            
    # Functions to calculate the value functions and probabilities of each turn
        
    def calculate_turn_3(self, node_tree):
        # Calculate the value function and probabilities of the third turn with given order and begin state
        
        value_function_turn3 = calculate_value_function_turn3(node_tree,self.t,self.value_function_tp1)
        probability_dictionary_turn3 = calculate_probability_dictionary_turn3(node_tree,value_function_turn3,self.utility_functions)
        
        return value_function_turn3, probability_dictionary_turn3
    
    def calculate_turn_2(self, node_tree, value_function_turn3, probability_dictionary_turn3):
        # Calculate the value function and probabilities of the second turn with given order and begin state
        
        value_function_turn2 = calculate_value_function_turn2(node_tree,value_function_turn3, probability_dictionary_turn3)
        probability_dictionary_turn2 = calculate_probability_dictionary_turn2(node_tree,value_function_turn2,self.utility_functions)
        
        return value_function_turn2, probability_dictionary_turn2
    
    def calculate_turn_1(self, node_tree, value_function_turn2, probability_dictionary_turn2):
        # Calculate the value function and probabilities of the first turn with given order and begin state
        
        value_function_turn1 = calculate_value_function_turn1(node_tree,value_function_turn2, probability_dictionary_turn2)
        probability_dictionary_turn1 = calculate_probability_dictionary_turn1(node_tree,value_function_turn1,self.utility_functions)
        
        return value_function_turn1, probability_dictionary_turn1
        
    def generate_node_tree(self,begin_state,ordering):
        # Generates tree of nodes in given state and ordering and classifies parent and children of nodes
        
        node_tree = dict()
        
        node_tree[constants.A1_NODE_DEPTH] = list()
        node_tree[constants.A2_NODE_DEPTH] = list()
        node_tree[constants.A3_NODE_DEPTH] = list()
        
        player_first_turn = ordering[0]
        player_second_turn = ordering[1]
        player_third_turn = ordering[2]   
        
        possible_actions_turn1 = self.get_possible_player_actions(begin_state, player_first_turn)
        
        actions_before_round = (None,None,None)
        
        for action_turn1 in possible_actions_turn1:
            state_after_turn1 = self.transition_state(begin_state, action_turn1, player_first_turn)
            possible_action_turn2 = self.get_possible_player_actions(state_after_turn1,player_second_turn)
            
            
            # Place first level node in tree
            actions_after_turn1 = self.get_actions(actions_before_round,action_turn1,player_first_turn)
            node_turn1 = Node(begin_state,ordering,actions_after_turn1) 
            node_tree[constants.A1_NODE_DEPTH].append(node_turn1)
            
            for action_turn2 in possible_action_turn2:
                
                state_after_turn2 = self.transition_state(state_after_turn1,action_turn2, player_second_turn)
                possible_action_turn3 = self.get_possible_player_actions(state_after_turn2,player_third_turn)
                
                # Place second level node in tree
                actions_after_turn2 = self.get_actions(actions_after_turn1,action_turn2,player_second_turn)
                node_turn2 = Node(begin_state,ordering,actions_after_turn2)
                node_tree[constants.A2_NODE_DEPTH].append(node_turn2)
                         
                # Place second level node in children of first level node     
                node_turn1.children.append(node_turn2)
                # Store first level node as the parent of second level node
                node_turn2.parent = node_turn1
                
                for action_turn3 in possible_action_turn3:
                    
                    # Place third level node in tree
                    actions_after_turn3 = self.get_actions(actions_after_turn2,action_turn3,player_third_turn)
                    node_turn3 = Node(begin_state,ordering,actions_after_turn3)
                    node_tree[constants.A3_NODE_DEPTH].append(node_turn3)
                             
                    # Place third level node in children of second level node
                    node_turn2.children.append(node_turn3)
                    # Store second level node as the parent of third level node
                    node_turn3.parent = node_turn2
                    
        
        return node_tree
            
    def transition_state(self,state,action,player_turn):
        state_content_after_turn = list(state.state_content)
        state_content_after_turn[player_turn] = action
        state_after_turn = State(tuple(state_content_after_turn))
        return state_after_turn
    
    def get_actions(self,actions,action,player_turn):
        actions_after_turn = list(actions)
        actions_after_turn[player_turn] = action
        return tuple(actions_after_turn)
    
    def get_possible_player_actions(self, begin_state, player_turn):
        turn_state = TurnState(begin_state, player_turn)
        possible_actions = self.action_space[turn_state]
        return possible_actions