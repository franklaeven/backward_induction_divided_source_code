import constants
from states import State
from states import TurnState
from copy import copy

def populate_state_space():
    candidates = [(s1,s2,s3) for s1 in constants.ACTIONS 
                  for s2 in constants.ACTIONS 
                  for s3 in constants.ACTIONS]     
    viable_states = []
    for candidate in candidates:
        s = State(candidate)
        if s.is_viable:
            viable_states.append(s)
    return viable_states

def populate_turn_state_space(state_space, players_space):
    turn_state_space = [TurnState(copy(state), current_player) for state in state_space
                         for current_player in players_space]
    return turn_state_space

def get_state_index_dictionary(state_space):
    return {state:i for i,state in enumerate(state_space)}

def populate_action_dictionary(turn_state_space, state_space):
    #Populates actions to all possible turn states
    action_dictionary = dict()
    for turn_state in turn_state_space:
        current_player = turn_state.player_turn
        current_state = turn_state.state
        current_claim = current_state[current_player]
        action_candidates = lower_claims(current_claim)
        viable_actions = list()
                        
        for action in action_candidates:
            new_state_contents = list(current_state.state_content)
            new_state_contents[current_player] = action
            new_state = State(tuple(new_state_contents))
            if new_state in state_space:
                viable_actions.append(action)
        action_dictionary[turn_state] = tuple(viable_actions)
    return action_dictionary

def populate_diminished_states(state):
    state_space = populate_state_space()
    diminished_state_space = []
    for end_state in state_space:
        if isReachable(state,end_state):
            diminished_state_space.append(end_state)
    return diminished_state_space

def populate_diminished_state_space():
    state_space = populate_state_space()
    diminished_state_space = dict()
    for state in state_space:
        diminished_state_space[state] = populate_diminished_states(state)
    return diminished_state_space

def lower_claims(claim):
    claim_index = constants.ACTIONS.index(claim)
    return constants.ACTIONS[claim_index:]

def transition_state(state,action,player):
    state_content = list(state.state_content)
    state_content[player] = action
    transitioned_state = State(tuple(state_content))
    return transitioned_state

def isReachable(start_state,end_state):
    isReachable = True
    for i,claim in enumerate(start_state.state_content):
        lc = lower_claims(claim)
        isReachable*=(end_state.state_content[i] in lc)
    return isReachable
    
    