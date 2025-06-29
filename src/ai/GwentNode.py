from src.ai.PlayerState import PlayerState
from src.ai.GameState import GameState
from src.ai.Node import Node


# we are inheriting from the abstract node class
class GwentNode(Node):

    def __init__(self, game_state, parent = None):
        self.game_state = game_state
        self.parent = parent
        #allowing duplicates in this scenario
        self.children = []
        self.visits = 0
        self.total_reward = 0.0


    def find_children(self):
        pass

    def find_random_child(self):
        pass

    def is_terminal(self):
        pass

    def reward(self):
        pass

    def __eq__(self, other):
        pass


