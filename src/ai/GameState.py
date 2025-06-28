from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen= True)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    weather_rows: Set[str]

