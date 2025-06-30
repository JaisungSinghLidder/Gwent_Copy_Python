from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set, List

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen= True)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    weather_rows: Set[str]

    #this class will handle what is playable in the AI player's hand
    
    def is_playable(self):
        pass

    def get_legal_moves(self) -> list:
        legal_moves = []

        pass





    def apply_move(self,move):
        pass

    def is_terminal(self) -> bool:
        pass

    def get_reward(self):
        pass

