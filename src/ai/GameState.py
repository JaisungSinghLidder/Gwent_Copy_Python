from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set


@dataclass(frozen= True)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    weather_rows: Set[str]

