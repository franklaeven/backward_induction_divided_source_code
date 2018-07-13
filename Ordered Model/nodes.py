from states import State

class Node:
    def __init__(self,begin_state,ordering,actions):
        
        assert type(begin_state) == State , "First argument must be of type State" 
        assert type(ordering) == tuple or type(ordering) == type(None), "Second argument must be of type tuple"
        assert type(actions) == tuple , "Third argument must be of type tuple"
        
        self.begin_state = begin_state
        self.ordering = ordering
        self.actions = actions
        
        self.action1 = actions[0]   # begin state is ordered in player order
        self.action2 = actions[1]   # ordering describes this order
        self.action3 = actions[2]   # actions are ordered in player order
        
        self.has_action3 = not(self.actions[2] == None)
        self.has_action2 = not(self.actions[1] == None)                         
        self.has_action1 = not(self.actions[0] == None)
        
        self.node_depth = self.node_depth()
        
        self.end_state = self.get_end_state()
        
        self.children = []
        self.siblings = []
        self.parent  = None
        
    def __eq__(self, other):
        return  None if other == None else \
                (self.begin_state == other.begin_state and
                self.actions == other.actions and
                self.ordering == other.ordering)
    
    def __hash__(self):
            return hash(self.begin_state) + hash(self.actions) + hash(self.ordering)
        
    def __str__(self):
        return 'Node( Begin state: ' + str(self.begin_state) + '\nOrdering: '+str(self.ordering)+'\nactions'+str(self.actions)+' )\n'
    
    def __repr__(self):
        return self.__str__() 
    
    def get_player_turn(self):
        return self.ordering[self.node_depth-2]
        
    def get_end_state(self):
        # Calculates the end state or current state the node is in after applying the players actions
        end_state_content = list()
        begin_state_content = self.begin_state.state_content
        
        for i, state in enumerate(begin_state_content):
            end_state_content.append(self.actions[i] if not self.actions[i] == None else begin_state_content[i])
        
        end_state = State(tuple(end_state_content))
            
        return end_state
    
    def node_depth(self): 
        # Checks the depth at which the node is in the tree. 0 means first turn node, 1 means second turn node and 2 means third and final turn node
        depth_of_node = self.has_action1+self.has_action2+self.has_action3 -1
        return depth_of_node
        