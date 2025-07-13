from typing import List, Dict
from src.cards.Card import Card
from src.cards.Deck import Deck
from src.general_game_space.Leader import Leader
from src.general_game_space.PlayerLogic import PlayerLogic

class Player:

    def __init__(self, deck: Deck, leader_card: Leader, faction: str, ai_player: bool, player_name: str):
        self.player_name = player_name
        self.deck = deck
        self.hand: List[Card] = []
        self.board: Dict[str, List[Card]] = {"melee": [], "range": [], "siege": []}
        #this is going to be where cards die!
        self.graveyard: List[Card] = []
        self.leader_card = leader_card
        self.faction = faction
        self.passed = False
        self.lives = 2
        self.leader_used = False
        #This will control whether who goes first or not
        #True will indicate that it is True
        self.turn_order_first = False
        self.ai_player = ai_player
        self.player_name = player_name
        #these bool statements will judge whether a row is being affected by a weather effect
        self.melee_row_weather_effect = False
        self.range_row_weather_effect = False
        self.siege_row_weather_effect = False
        #these statements will do the weather effects; however, it will be the commanding horn
        self.melee_row_horn_effect = False
        self.range_row_horn_effect = False
        self.siege_row_horn_effect = False
        #reintroducing player own sum
        self.sum = 0


    #adding a draw hand implementation later after typing is completed

    #do not need to import draw_card_to_hand
    def draw_card_to_hand(self) -> None:
        card = self.deck.draw_from_deck()
        if card is not None:
            self.hand.append(card)
        else:
            print(f"{self.player_name}'s deck is empty. No card drawn.")

    #need to port this over player logic
    def play_card(self, card_name: str) -> Card | None:

        PlayerLogic.play_card(self, card_name)

    #no need
    def lose_life(self) -> None:
        self.lives -= 1

    #no need
    def lose_game(self) -> str:
        if self.lives == 0:
            return "Defeated"

    #maybe?
    def check_lives(self) -> int:
        return self.lives

    #no need
    def display_hands(self) -> None:
        print("Displaying your hand")
        for card in self.hand:
            print(f"{card.card_name} | {card.strength} | {card.ability}")

        print("Displaying your side of the board")
        #use items() instead of enumerate as it will just return the key and not the item itself inside the dictionary
        for row, cards in self.board.items():
            print(f"\n{row.upper()}")
            for card in cards:
                print(f"{card.card_name} | {card.strength} | {card.ability}")

    #maybe
    def passing_turn(self) -> None:

        PlayerLogic.passing_turn(self)


    #no need
    def can_use_leader(self) -> bool:
        if not self.leader_used:
            return True
        else:
            return False
    #no need
    def round_end(self) -> None:
        for row in self.board.values():
            self.graveyard.extend(row)
            row.clear()
































