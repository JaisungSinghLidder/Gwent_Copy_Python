from copy import deepcopy
from typing import Union, Tuple

from src.ai.GwentNode import GwentNode
from src.ai.GameState import GameState
from src.cards.Card import Card
import math
import random




class MCTS:


    #you should imagine this class as a tree that is filled with Gwent Nodes.
    #we will search through the tree, create a process of backpropagation along the tree to eventually find the best node in the tree
    #I highly recommended using this links I had put in the ReadMe file to understand how a MCTS works


    #searches through to find the best possible for the tree
    #the main driver function where it will contain every other functions
    def search(self, root: GwentNode, num_simulations: int) -> GwentNode:
        for _ in range(num_simulations):
            node = self.selection(root)
            if not node.is_expanded:
                node = self.expansion(node)
            reward = self.rollout(node)
            self.backpropagate(node, reward)

        best_child = max(root.children, key=lambda c: c.visits)
        return best_child


    #we are going to navigate the tree using the UCT formula to find a promising node to expand
    #it will go along until it finds a leaf
    def selection(self, node: GwentNode) -> GwentNode:

        current = node
        while current.is_expanded:
            current = current.best_child()

        return current

    #add more child nodes to the tree from the selected node
    def expansion(self, node: GwentNode) -> GwentNode:

        #when there is terminal, then just return the node
        if node.is_terminal():
            return node

        node.find_children()

        node.is_expanded = True

        return random.choice(node.children)


    #UCT OR "UPPER CONFIDENCE BOUND APPLIED TO TREES" is an essential formula we will be using
    def best_uct(self, node: GwentNode) -> GwentNode:

        best_score = float('-inf')

        best_child = None

        for child in node.children:
            if child.visits == 0:
                #if we haven't visited the child, then it is going to be an infinity amount
                uct_score  = float('inf')
            else:
                #creating the uct score calculation
                uct_score = child.Q() + child.U()


            if uct_score > best_score:
                best_score = uct_score
                best_child = child

        return best_child


    #the rollout is going to be a simulation of a game state and will give us a reward based on that random game state
    #might be bad implementation, current rollout is O(n^3), which is terrible

    def rollout(self, node: GwentNode) -> float:


        sim_state = deepcopy(node.game_state)

        state_reward = 0

        terminal_state = False


        current_player = sim_state.ai_player_state

        other_player = sim_state.opponent_state

        while not sim_state.is_terminal():

            if not current_player.passed:

                legal_moves = sim_state.get_legal_moves(current_player)

                if legal_moves:

                    move = sim_state.get_random_move(legal_moves)

                    if isinstance(move, tuple):

                        sim_state = sim_state.apply_move(move[0], move[1], current_player)

                        terminal_state = sim_state.is_terminal()

                        state_reward += sim_state.get_reward(terminal_state)

                    else:

                        sim_state = sim_state.apply_move(move, None,  current_player)

                        terminal_state = sim_state.is_terminal()

                        state_reward += sim_state.get_reward(terminal_state)
                else:

                    sim_state = sim_state.apply_move("PASS", None, current_player)

                    terminal_state = sim_state.is_terminal()

                    state_reward += sim_state.get_reward(terminal_state)


            current_player, other_player = other_player, current_player

        terminal_state = sim_state.is_terminal()

        state_reward += sim_state.get_reward(terminal_state)

        return state_reward




    #this is going to propagate the result of the rollout all the way up the tree so that it can update the counts and reward
    def backpropagate(self, node: GwentNode, reward: float) -> None:
        current = node
        flip = 1
        while current is not None:
            current.visits += 1
            current.total_reward += flip * reward
            flip *= -1
            current = current.parent




    def get_move_from_node(self, node: GwentNode) -> Union[str, Card, Tuple[str, Card]]:
        return node.move