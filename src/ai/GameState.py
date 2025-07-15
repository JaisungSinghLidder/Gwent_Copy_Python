from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set, List, Union

from src.general_game_space.GameLogic import GameLogic
from src.general_game_space.PlayerLogic import PlayerLogic
from src.cards.Card import Card
from copy import deepcopy

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen = False)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    active_weather_effect: Set[str]

    #this class will handle what is playable in the AI player's hand
    #the AI need this class because it needs to be able to discern what it can do so that when it generates the tree
    #isn't filled with wrong moves
    #IMPLEMENTATION_NOTE: this method need to be pretty comprehensive and prevent any illegal moves

    def get_legal_moves(self) -> List[Union[Card, str]]:
        legal_moves = []

        #this case is for the leader
        #we are going to append a string because using a leader card is a special case
        if not self.ai_player_state.leader_used:
            legal_moves.append("USE_LEADER")

        # running through the cards through the hand
        for card in self.ai_player_state.hand:

            #checking here if the medic card can target any graveyard card
            if card.ability == "medic":
                if not self.ai_player_state.graveyard:
                    continue
            #checking the cards here
            legal_moves.append(card)

            #we need to append the commander horn ability
            if card.ability == "horn":
                for row in ["melee", "range", "siege"]:
                    row_cards = self.ai_player_state.board[row]
                    #appending the row so that we can bring over the row as well
                    legal_moves.append((card,row))


            #I should apply the other words here that have other abilites


        #allowing the passing the turn
        legal_moves.append("PASS")


        return legal_moves


    #lots of integration with the apply moves
    def apply_move(self, move: Union[Card, str]) -> "GameState":
        new_state = deepcopy(self)

        if isinstance(move, str):
            if move == "PASS":
                new_state.ai_player_state.passed = True

            #need to play leader
            elif move == "USE_LEADER":
                new_state.ai_player_state.leader_used = True

        if isinstance(move, Card):
            #need to use the player logic
            #the basic unit
            if move.ability == "unit":

                PlayerLogic.play_card(new_state.ai_player_state, move.card_name)

            elif move.ability == "weather":

                GameLogic.check_weather_effect_MCTS(new_state, move.card_name)

            elif move.ability == "buff":

                GameLogic.check_buff_logic(new_state, new_state.ai_player_state, move)



        return new_state


    def is_terminal(self) -> bool:
        pass

    def get_reward(self):
        pass

