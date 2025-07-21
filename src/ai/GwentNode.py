from typing import Union, List
from src.ai.PlayerState import PlayerState
from src.ai.GameState import GameState
from src.cards.Card import Card
from src.ai.Node import Node
#debugging it by adding imports
import numpy as np
import math



# we are inheriting from the abstract node class
class GwentNode(Node):

    def __init__(self, game_state, parent = None):
        self.game_state = game_state
        self.parent = parent
        #allowing duplicates in this scenario
        self.children = []
        self.visits = 0
        self.total_reward = 0.0
        #checking here if it's node has been expanded
        self.is_expanded = False

    #so this is to find the next legal moves in the position
    #use the return of the list that the game state creates

    def find_children(self) -> None:


        #getting a list of all the legal moves that can happen within the game
        legal_moves = self.game_state.get_legal_moves()

        #going through and picking up a move in legal moves
        for move in legal_moves:
            #checking whether the class is a tuple, because it will then have that row variable beside it

            if isinstance(move, tuple):

                #extracting the move/card
                play_move = move[0]

                #extracting the row
                play_row = move[1]

                #creating a new state
                new_state = self.game_state.apply_move(play_move, play_row)
                #now creating a child node
                #where this node is now it's parent
                child_node = GwentNode(new_state, parent = self)
                #now appending the child node
                self.children.append(child_node)

            #regular case
            else:

                new_state = self.game_state.apply_move(move)
                # now creating a child node
                # where this node is now it's parent
                child_node = GwentNode(new_state, parent=self)
                # now appending the child node
                self.children.append(child_node)










    #to randomly pick a legal move child
    def find_random_child(self):
        pass

    #deciding whether it is terminal
    def is_terminal(self) -> bool:
        return self.game_state.is_terminal()

    def reward(self) -> float:
        return self.game_state.reward()

    def __eq__(self, other: GameState) -> bool:
        if not isinstance(other, GwentNode):
            return False

        return self.game_state == other.game_state


    def __hash__(self):
        hash(self.game_state)

    def Q(self) -> float:
        return self.total_reward / (1 + self.visits)

    def U(self) -> float:
        pass

    # this just selects the most promising move (aka the best child GwentNode)

    def best_child(self, node: "GwentNode") -> "GwentNode":
        pass

