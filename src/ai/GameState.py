from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set, List, Union
from src.cards.Card import Card
from copy import deepcopy

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen= False)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    weather_rows: Set[str]

    #this class will handle what is playable in the AI player's hand
    #the AI need this class because it needs to be able to discern what it can do so that when it generates the tree
    #the tree isn't filled with wrong moves
    #IMPLEMENTATION_NOTE: this method need to be pretty comprehensive and prevent any illegal moves

    def get_legal_moves(self) -> List[Union[Card, str]]:
        legal_moves = []

        #this case is for the leader
        #we are going to append a string because using a leader card is a special case
        if not self.ai_player_state.leader_used:
            legal_moves.append("USE_LEADER")

        # running through the cards through the hand
        for card in self.ai_player_state.hand:
            #checking the cards here
            legal_moves.append(card)


        #allowing the passing the turn
        legal_moves.append("PASS")


        return legal_moves



    def apply_move(self, move: Union[Card, str]) -> "GameState":
        new_state = deepcopy(self)

        if move == "PASS":
            new_state.ai_player_state.passed = True


        elif move == "USE_LEADER":
            new_state.ai_player_state.leader_used = True

        elif isinstance(move, Card):
            new_state.ai_player_state.hand.remove(move)
            new_state.ai_player_state.board[move.row].append(move)

        return new_state



    def is_terminal(self) -> bool:
        pass

    def get_reward(self):
        pass

