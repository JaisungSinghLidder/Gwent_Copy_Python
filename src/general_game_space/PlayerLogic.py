
from src.ai.PlayerState import PlayerState
from src.cards.Card import Card
from typing import Union, Optional



class PlayerLogic:

    @staticmethod
    def play_card(player_or_player_state: Union["Player", PlayerState], card_name: str) -> Card | None:
        from src.general_game_space.Player import Player

        card_name = card_name.lower().strip()

        if isinstance(player_or_player_state, Player):
            if not player_or_player_state.hand:
                print("DEBUG: HAND IS EMPTY")
                return None

            for i, card in enumerate(player_or_player_state.hand):
                if card.card_name.lower().strip() == card_name:
                    # Safely remove card first
                    played_card = player_or_player_state.hand.pop(i)

                    # Then append it to board or graveyard
                    if played_card.card_type.lower().strip() in ["unit", "hero"]:
                        player_or_player_state.board[played_card.row].append(played_card)
                    else:
                        player_or_player_state.graveyard.append(played_card)

                    return played_card

            print("DEBUG: CARD NOT FOUND IN HAND")
            return None

        elif isinstance(player_or_player_state, PlayerState):
            if not player_or_player_state.hand:
                return None

            for i, card in enumerate(player_or_player_state.hand):
                if card.card_name.lower().strip() == card_name:
                    played_card = player_or_player_state.hand.pop(i)

                    if played_card.card_type.lower().strip() in ["unit", "hero"]:
                        player_or_player_state.board[played_card.row].append(played_card)
                    else:
                        player_or_player_state.graveyard.append(played_card)

                    return played_card

            return None

        else:
            raise ValueError("Need to enter either a Player or PlayerState instance")

    @staticmethod
    def passing_turn(player_or_player_state: Union["Player", PlayerState], passChoice: Optional[str]) -> None:
        from src.general_game_space.Player import Player

        if isinstance(player_or_player_state, Player):

            while True:
                choice = input("Do you want to pass this round: yes or no?").lower()
                if choice.lower().strip() == "yes":
                    player_or_player_state.passed = True
                    break
                elif choice.lower().strip() == "no":
                    player_or_player_state.passed = False
                    break
                else:
                    print("Please input either yes or no?")

        elif isinstance(player_or_player_state, PlayerState):

            if passChoice.lower().strip() == "yes":
                player_or_player_state.passed = True

            elif passChoice.lower().strip() == "no":
                player_or_player_state.passed = False




