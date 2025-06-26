from typing import List

from Card import Card
import json
import random

from Card_Space.Card import Card
from Card_Space.CardLoader import CardLoader


class Deck:
    def __init__(self, faction_name: str) -> object:
        #storing how many cards
        self.cards: List[Card] = []
        self.faction_name = faction_name

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def check_faction_deck(self) -> bool:
        for card in self.cards:
            if card.faction != self.faction_name and card.faction != "neutral":
                return False
        return True

    def load_card_from_db(self, path: str):
        self.cards = CardLoader.load_card_from_db(path, self.faction_name)


    #Limiting deck to 10 cards for now
    def check_deck_size(self) -> bool:
        if len(self.cards) == 10:
            return True
        return False

    def add_to_deck(self, card) -> None:
        self.cards.append(card)

    def subtract_from_deck(self, card) -> None:
        for i, c in enumerate(self.cards):
            #this checks if it is the same object in memory
            if c is card:
                del self.cards[i]
                break

    def draw_from_deck(self) -> Card | None:
        if not self.cards:
            print("There is no cards to draw")
            return None
        else:
            random_card = random.randint(0, len(self.cards) - 1 )
            return self.cards.pop(random_card)


