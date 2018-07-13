from utility_functions import envy__guilt_utility_function_player

from games import Game

from data_analysis_functions import get_probability_data
from data_analysis_functions import get_value_data

import matplotlib.pyplot as plt


def main():
    
    # Define the envy constants of the utility function in relation to the other players
    envy_constants_player1 = (0,.4,.3)
    envy_constants_player2 = (.4,0,.2)
    envy_constants_player3 = (.5,.3,0)
    
    # Define the guilt constants of the utility function in relation to the other players
    guilt_constants_player1 = (0,.2,.1)
    guilt_constants_player2 = (.3,0,.1)
    guilt_constants_player3 = (.7,.4,0)
    
    # Define the utility functions for each of the players
    utility1 = lambda x, p: envy__guilt_utility_function_player(x , p, envy_constants_player1, guilt_constants_player1)
    utility2 = lambda x, p: envy__guilt_utility_function_player(x , p, envy_constants_player2, guilt_constants_player2)
    utility3 = lambda x, p: envy__guilt_utility_function_player(x , p, envy_constants_player3, guilt_constants_player3)
    
    # Store these utility functions in a list
    utility_functions = [utility1, utility2, utility3]
    
    #Create an instance of the bargaining game with the required utility functions
    game = Game(utility_functions)
    game.simulate_game()
    
    #Exctract the value functions of every time step and the state transition probabilites at every time step
    value_functions = game.value_functions
    probability_matrices = game.probability_matrices
    
    x_data_v, y_data_v, x_label_v, y_label_v, legend_labels_v, plot_title_v = \
                                                get_value_data(value_functions)
    x_data_p, y_data_p, x_label_p, y_label_p, legend_labels_p, plot_title_p = \
                                     get_probability_data(probability_matrices)    
    
    # Plot value functions of state "(A,A,A)"
    plt.figure(1)
    plt.plot(x_data_v, y_data_v)
    plt.xlabel(x_label_v)
    plt.ylabel(y_label_v)
    plt.legend(legend_labels_v)
    plt.title(plot_title_v)
    
     # Plot probability of consensus for begin state "(A,A,A)"
    plt.figure(2)
    plt.plot(x_data_p, y_data_p)
    plt.xlabel(x_label_p)
    plt.ylabel(y_label_p)
    plt.legend(legend_labels_p)
    plt.title(plot_title_p)
    
    
    
if __name__ == "__main__":
    main()