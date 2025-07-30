from dataclasses import dataclass, field
from typing import Dict, Tuple, List
from src.cards.Card import Card
from src.general_game_space.Leader import Leader

#a dataclass that should provide a snapshot view of the players' information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen=False)
class PlayerState:

    hand: List[Card]
    graveyard: List[Card]
    lives: int
    board: Dict[str, List[Card]]
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
    opponent_hand: List[Card] = field(default_factory=list)

    def clone(self):
        return PlayerState(
            hand=[card.clone() for card in self.hand],
            graveyard=[card.clone() for card in self.graveyard],
            board={row: [card.clone() for card in cards] for row, cards in self.board.items()},
            passed=self.passed,
            sum=self.sum,
            leader_used=self.leader_used,
            leader = self.leader_card.clone(),
            faction=self.faction,
            ai_player = self.ai_player,
            player_name= self.player_name,
            melee_row_weather_effect = self.melee_row_weather_effect,
            range_row_weather_effect= self.siege_row_weather_effect,
            siege_row_weather_effect= self.siege_row_weather_effect,
            melee_row_horn_effect= self.melee_row_horn_effect,
            range_row_horn_effect= self.range_row_horn_effect,
            siege_row_horn_effect= self.siege_row_horn_effect,
            opponent_hand = [card.clone() for card in self.opponent_hand]
        )



















