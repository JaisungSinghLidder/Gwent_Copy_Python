from typing import Union, List
from src.ai.PlayerState import PlayerState
from src.ai.GameState import GameState
from src.cards.Card import Card
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

    #so this is to find the next legal moves in the position
    #use the return of the list that the game state creates

    def find_children(self, legal_moves: List[Union[Card, str]]):
        pass

    #to randomly pick a legal move child
    def find_random_child(self):
        pass

    #deciding whether it is terminal
    def is_terminal(self):
        return self.game_state.is_terminal()

    def reward(self):
        return self.game_state.reward()

    def __eq__(self, other):
        pass


