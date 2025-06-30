from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set, List
from src.cards.Card import Card

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen= True)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    weather_rows: Set[str]

    #this class will handle what is playable in the AI player's hand
    #the AI need this class because it needs to be able to discern what it can do so that when it generates the tree
    #the tree isn't filled with wrong moves
    #IMPLEMENTATION_NOTE: this class need to be pretty comprehensive and prevent any illegal moves

    def is_playable(self, card: Card) -> bool:

        if card.card_type  == "leader" and self.ai_player_state.leader_used:
            return False






        #it passed all the failed checks
        return True




    def get_legal_moves(self) -> list:
        legal_moves = []

        pass





    def apply_move(self,move):
        pass

    def is_terminal(self) -> bool:
        pass

    def get_reward(self):
        pass

