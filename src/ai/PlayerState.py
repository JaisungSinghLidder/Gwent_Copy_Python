from dataclasses import dataclass
from typing import Dict, Tuple, List
from src.cards.Card import Card
from src.general_game_space.Leader import Leader

#a dataclass that should provide a snapshot view of the players' information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen=False)
class PlayerState:

    hand: List[Card, ...]
    graveyard: List[Card, ...]
    lives: int
    board: Dict[str, List[Card, ...]]
    passed: bool
    sum: int
    leader_used: bool
    leader_card: Leader
    faction: str
    ai_player: bool
    player_name: str
    melee_row_weather_effect : bool
    range_row_weather_effect : bool
    siege_row_weather_effect : bool
    melee_row_horn_effect : bool
    range_row_horn_effect : bool
    siege_row_horn_effect : bool














