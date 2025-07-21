from src.ai.GwentNode import GwentNode




class MCTS:

    def __init__(self):
        pass


    def search(self, root: GwentNode, num_simulations: int) -> GwentNode:
        pass

    def selection(self, node: GwentNode) -> GwentNode:
        pass

    def expansion(self, node: GwentNode) -> GwentNode:
        pass

    def best_uct(self, node: GwentNode) -> GwentNode:
        pass

    def rollout(self, node: GwentNode) -> float:
        pass


    def backpropagation(self, node:GwentNode, reward: float) -> None:
        pass

    def best_child(self, node: GwentNode) -> GwentNode:
        pass