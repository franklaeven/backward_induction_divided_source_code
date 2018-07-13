import numpy as np

def envy__guilt_utility_function_player(values, current_player, envy_constants, guilt_constants):
    
    value_current_player = values[current_player]
    
    value_differences = [value-value_current_player for value in values]

    has_more_value_list = [int(value_difference>0) for value_difference in value_differences]
    has_less_value_list = [int(value_difference<0)  for value_difference in value_differences]
    
    envy_utility_list = [value_difference*has_more_value_list[i]*envy_constants[i] for i, value_difference in enumerate(value_differences)]
    guilt_utility_list = [-value_difference*has_less_value_list[i]*guilt_constants[i] for i, value_difference in enumerate(value_differences)]
    
    utility_current_player = value_current_player
    
    for envy_utility in envy_utility_list:
        utility_current_player -= envy_utility
        
    for guilt_utility in guilt_utility_list:
        utility_current_player -= guilt_utility
    
                                           
    return utility_current_player

