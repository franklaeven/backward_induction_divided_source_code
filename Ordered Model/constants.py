ACTIONS = ("A","B","C")
ACTIONS_TO_NUMBERS = {"A":0,"B":1,"C":2}
N_PLAYERS = 3
ACTION_VALUES = (0,2,3)
CONSENSUS_CONSTANT = 5
ACTION_WEIGHTS = dict(zip(ACTIONS,ACTION_VALUES))
RECOGNITION_PROBABILITIES = {0:1/3, 1:1/3, 2:1/3}
PAYOFF_DICTIONARY = {"A":.65,"B":.25,"C":.1}

CONSENSUS_STATES = (5,7,10,12,14,15)

RATIONALITY_CONSTANT = 50

TOTAL_TIME = 20

TIME_STEP = 100/TOTAL_TIME

ORDERING_SPACE = [(0,1,2),(0,2,1),(1,0,2),(1,2,0),(2,0,1),(2,1,0)]

A3_NODE_DEPTH = 2
A2_NODE_DEPTH = 1
A1_NODE_DEPTH = 0
ORDERING_NODE_DEPTH = -1
STATE_NODE_DEPTH = -2