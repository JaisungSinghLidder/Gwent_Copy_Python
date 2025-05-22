from Card_Space.Card import Card
from Card_Space.Deck import Deck

class Player:

    def __init__(self, hand, leader_card, strength, faction, ai_player, player_name, weather_sum, sum):
        self.player_name = player_name
        self.deck = []
        self.hand = hand
        self.board = {"melee": [], "ranged": [], "siege": []}
        #this is going to be where cards die!
        self.graveyard = []
        self.leader_card = leader_card
        self.strength = strength
        self.faction = faction
        self.passed = False
        self.lives = 2
        self.leader_used = False
        #This will control whether who goes first or not
        #True will indicate that it is True
        self.turn_order_first = False
        self.ai_player = ai_player
        self.player_name = player_name
        self.weather_sum = weather_sum
        self.sum = sum



    def play_card(self, card_name):

        if not self.hand:
            print("You have nothing in your hand")
            return None

        else:
            for i, card in enumerate(self.hand):
                #card is a unit and it exists in hand
                if card.card_name == card_name and card.card_type == "unit":
                    self.strength += card.strength
                    self.board[card.row].append(card)
                    return self.hand.pop(i)
                #case where it is a weather card, this is important as weather cards affect both boards so it needs special handling
                elif card.card_name == card_name and card.card_type == "weather":
                    self.graveyard.append(card)
                    return self.hand.pop(i)
                else:
                    print("That card doesn't exist")
                    return None


    def reset_score(self):
        self.strength = 0

    def lose_life(self):
        self.lives -= 1

    def lose_game(self):
        if self.lives == 0:
            return "Defeated"

    def check_lives(self):
        return self.lives

    def display_hand(self):
        print("Displaying your hand")
        for card in self.hand:
            print(f"{card.card_name} | {card.strength} | {card.ability}")

        print("Displaying your side of the board")
        #use items() instead of enumerate as it will just return the key and not the item itself inside the dictionary
        for row, cards in self.board.items():
            print(f"\n{row.upper()}")
            for card in cards:
                print(f"{card.card_name} | {card.strength} | {card.ability}")

    def passing_turn(self):
        passLoop = False
        while not passLoop:
            choice = input("Do you want to pass this round: yes or no?").lower()
            if choice == "yes":
                self.passed = True
                passLoop = True
            elif choice == "no":
                self.passed = False
                passLoop = True
            else:
                print("Please input either yes or no?")

    def can_use_leader(self):
        if not self.leader_used:
            return True
        else:
            return False

    def round_end(self):
        for row in self.board.values():
            self.graveyard.extend(row)
            row.clear()
        self.weather_sum = 0
        self.sum = 0







