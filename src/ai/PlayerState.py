from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from src.cards.Card import Card
from src.general_game_space.Leader import Leader

#a dataclass that should provide a snapshot view of the players' information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen=True)
class PlayerState:

    hand: Tuple[Card, ...]
    graveyard: Tuple[Card, ...]
    lives: int
    board: Dict[str, Tuple[Card, ...]]
    passed: bool
    sum: int
    leader_used: bool
    leader_card: Leader
    faction: str
    ai_player: bool













