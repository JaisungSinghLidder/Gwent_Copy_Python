from src.general_game_space import Game, Player
from src.ai.PlayerState import PlayerState
from src.cards.Card import Card
from typing import Union, Optional



class PlayerLogic:

    def play_card(player_or_player_state: Union[Player, PlayerState], card_name: str) -> Card | None | str:


        #change logic to separate AI and human player code


        if isinstance(player_or_player_state, Player):
            while True:
                if not player_or_player_state.hand:
                    print("You have nothing in your hand")
                    return None

                for i, card in enumerate(player_or_player_state.hand):
                    if card.card_name.lower().strip() == card_name.lower().strip():
                        if card.card_type.lower().strip() == "unit":
                            player_or_player_state.board[card.row].append(card)
                            return player_or_player_state.hand.pop(i)
                        elif card.card_type.lower().strip() == "weather":
                            player_or_player_state.graveyard.append(card)
                            return player_or_player_state.hand.pop(i)
                        # note to myself, create a case for this
                        elif card.card_type.lower().strip() == "buff":
                            player_or_player_state.graveyard.append(card)
                            return player_or_player_state.hand.pop(i)

                print("That card doesn't exist, please try again")
                card_name = input("Enter a valid card name:")

        elif isinstance(player_or_player_state, PlayerState):

            if not player_or_player_state.hand:
                return "You have nothing in your hand"

            for i, card in enumerate(player_or_player_state.hand):
                if card.card_name.lower().strip() == card_name.lower().strip():
                    if card.card_type.lower().strip() == "unit":
                        player_or_player_state.board[card.row].append(card)
                        return player_or_player_state.hand.pop(i)
                    elif card.card_type.lower().strip() == "weather":
                        player_or_player_state.graveyard.append(card)
                        return player_or_player_state.hand.pop(i)
                    # note to myself, create a case for this
                    elif card.card_type.lower().strip() == "buff":
                        player_or_player_state.graveyard.append(card)
                        return player_or_player_state.hand.pop(i)
                    