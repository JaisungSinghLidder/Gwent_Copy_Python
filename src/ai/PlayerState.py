from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from src.cards.Card import Card
from src.general_game_space.Leader import Leader



@dataclass(frozen=True)
class PlayerState:

    hand: Tuple[Card, ...]
    graveyard: Tuple[Card, ...]
    lives: int
    board: Dict[str, Tuple[Card, ...]]
    turn_order: bool
    sum: int
    leader_used: bool
    leader_card: Leader
    faction: str
    passed: bool
    ai_player: bool













