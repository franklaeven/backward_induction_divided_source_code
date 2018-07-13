import constants

from space_functions import populate_state_space
from space_functions import populate_turn_state_space
from space_functions import populate_action_dictionary

from nodes import Node

from rounds import Round

class Game:
    def __init__(self, utility_functions):
        
        self.utility_functions = utility_functions
        
        self.state_space = populate_state_space()
        self.player_space = [i for i in range(constants.N_PLAYERS)]
        self.turn_state_space = populate_turn_state_space(self.state_space,self.player_space)
        self.action_space = populate_action_dictionary(self.turn_state_space,self.state_space)
        
        value_function_t_end = dict()
        
        for state in self.state_space:
            value_function_t_end[Node(state, None, (None, None, None))] = [0,0,0]
            
        self.value_functions = {constants.TOTAL_TIME + 1 : value_function_t_end}
        self.probability_matrices = dict()
        
    def simulate_game(self):
        
        for t in range(constants.TOTAL_TIME,-1,-1):
            r_t = Round(t, self.state_space, self.action_space, self.value_functions[t+1], self.utility_functions)
            r_t.calculate_round()
            self.value_functions[t] = r_t.value_function_t
            self.probability_matrices[t] = r_t.probability_matrix