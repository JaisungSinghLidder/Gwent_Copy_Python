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
    #this will also filter out bad moves that serve no purpose
    def get_legal_moves(self) -> List[Union[Card, str]]:
        legal_moves = []

        #this case is for the leader
        #we are going to append a string because using a leader card is a special case
        # now we need to check for faction and illegal moves for that faction in tow
        if not self.ai_player_state.leader_used:

            #okay now we need to check for behaviour of players
            #might need to create a sub function

            #northen realms is going to be a simple weather check
            if self.ai_player_state.faction == "northern realms":
                if not self.active_weather_effect:
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
            #what to do here, this here needs to change
            #the logic is weak!
            if card.ability == "horn":
                #checking whether there are any cards in the ai's board
                has_any_cards = any(self.ai_player_state.board[row] for row in ["melee", "range", "siege"])

                #skip this card if there is no card on the board period
                if not has_any_cards:
                    continue

                if any(self.ai_player_state.board["melee"]):
                    horn_row = "melee"
                    legal_moves.append((card,horn_row))

                if any(self.ai_player_state.board["range"]):
                    horn_row = "range"
                    legal_moves.append((card, horn_row))

                if any(self.ai_player_state.board["siege"]):
                    horn_row = "siege"
                    legal_moves.append((card, horn_row))




            #going to make it illegal for the ai that if the no cards, it shouldn't play scorch
            #also if there is only hero cards, as hero cards are unaffected by scorch
            if card.ability == "scorch":
                # Assume that all cards are heroes until proven otherwise
                only_heroes = True

                #checking if there is any cards in the opponent state
                has_any_cards = any(self.opponent_state.board[row] for row in ["melee", "range", "siege"])

                #if the opponent has no cards, then why bother with scorching it?
                if not has_any_cards:
                    continue


                for row in ["melee", "range","siege"]:
                    for opponent_card in self.opponent_state.board[row]:
                        if opponent_card.ability != "hero":
                            only_heroes = False
                            break

                    if not only_heroes:
                        break



                if not only_heroes:
                    legal_moves.append(card)


            if card.card_type == "weather":

                if card.card_name not in self.active_weather_effect:
                    legal_moves.append(card)




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

