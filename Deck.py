from Card import Card
import random
class Deck:
    def __init__(self, faction_name):
        #storing how many cards
        self.cards = []
        self.faction_name = faction_name

    def shuffle(self):
        random.shuffle(self.cards)

    def check_faction_deck(self):
        for card in self.cards:
            if card.faction_name != self.faction_name and card.faction_name != "neutral":
                return False
        return True

    #Limiting deck to 10 cards for now
    def check_deck_size(self):
        if len(self.cards) == 10:
            return True
        return False

    def add_to_deck(self, card):
        self.cards.append(card)

    def subtract_from_deck(self, card):
        for i, c in enumerate(self.cards):
            #this checks if it is the same object in memory
            if c is card:
                del self.cards[i]
                break

    def draw_from_deck(self):
        random_card = random.randint(0, len(self.cards))
        return self.cards.pop(random_card)

