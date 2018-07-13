import constants

class State:
    def __init__(self, state_content):
        assert type(state_content) == tuple
        self.state_content = state_content
        self.state_weight = self.weight()
        self.is_viable = self.state_weight <= constants.CONSENSUS_CONSTANT
        self.is_consensus = self.state_weight == constants.CONSENSUS_CONSTANT
    
    def __str__(self):
        return 'State(' + str(self.state_content) + ')'
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, index):
        return self.state_content[index]
    
    def __setitem__(self, index, value):
        self.state_content[index] = value
    
    def __hash__(self):
        return hash(self.state_content)
    
    def __eq__(self, other):
        return self.state_content == None if other == None else self.state_content == other.state_content
    
    def __neq__(self, other):
        return not self==other
    
    def __ge__(self, other):
        a2n = constants.ACTIONS_TO_NUMBERS
        claim_ge = False
        for claim_this, claim_other in zip(self.state_content, other.state_content):
            claim_ge &= a2n[claim_this] >= a2n[claim_other]
        return claim_ge
    
    def __gt__(self, other):
        return (self >= other) and (self != other)
    
    def __le__(self, other):
        return (self >= other) and (self != other)
    
    def __lt__(self, other):
        return (self <= other) and (self != other)
    
    def weight(self):
        w = 0
        for i in self.state_content:
            w += constants.ACTION_WEIGHTS[i]
        return w
    
    def indices(self):
        indices_list = [constants.ACTIONS_TO_NUMBERS[claim] for claim in self.state_content]
        return tuple(indices_list)

class TurnState:
    def __init__(self, state, player_turn):
        #Player turn refers to the player that is about to make their move by index
        assert type(state) == State
        self.state = state
        self.player_turn = player_turn
    
    def __str__(self):
        return 'TurnState(' + str((self.state, self.player_turn)) + ')'
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.state) * hash(self.player_turn)
        
    def __eq__(self, other):
        return self.state == other.state and self.player_turn == other.player_turn
