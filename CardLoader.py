import json
from Card_Space.Card import Card
from Card_Space.Leader import Leader
import random

#this class will be handling the json file loading

class CardLoader:

    @staticmethod
    def load_card_from_json(path:str) -> list[Card]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Card(**item) for item in data]

    @staticmethod
    def load_leaders_from_json(path: str) -> list[Leader]:
        with open(path, "r") as f:
            data = json.load(f)
        return [Leader(**item) for item in data]

    @staticmethod
    def load_deck_from_json(path: str, faction: str,  deck_size: int = 20) -> list[Card]:
        cards = CardLoader.load_card_from_json(path)

        faction_cards = [card for card in cards if
                         card.faction == faction.lower().strip() or card.faction == "neutral"]

        cards = random.sample(faction_cards, deck_size)

        return cards

        return cards
