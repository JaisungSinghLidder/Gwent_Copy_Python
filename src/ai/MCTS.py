from src.ai.GwentNode import GwentNode
import math
import random




class MCTS:


    #you should imagine this class as a tree that is filled with Gwent Nodes.
    #we will search through the tree, create a process of backpropagation along the tree to eventually find the best node in the tree
    #I highly recommended using this links I had put in the ReadMe file to understand how a MCTS works

    def __init__(self):
        pass

    #searches through to find the best possible for the tree
    def search(self, root: GwentNode, num_simulations: int) -> GwentNode:
        pass

    #we are going to navigate the tree using the UCT formula to find a promising node to expand
    #it will go along until it finds a leaf
    def selection(self, node: GwentNode) -> GwentNode:
        pass

    #add more child nodes to the tree from the selected node
    def expansion(self, node: GwentNode) -> GwentNode:
        pass

    #UCT OR "UPPER CONFIDENCE BOUND APPLIED TO TREES" is an essential formula we will be using
    def best_uct(self, node: GwentNode) -> GwentNode:
        pass

    #the rollout is going to be a simulation of a game state and will give us a reward based on that random game state
    def rollout(self, node: GwentNode) -> float:
        pass

    #this is going to propagate the result of the rollout all the way up the tree so that it can update the counts and reward
    def backpropagation(self, node:GwentNode, reward: float) -> None:
        pass


