from typing import List

from src.ai.GameState import GameState
from src.general_game_space import Player
from src.cards.Card import Card
from src.general_game_space.GameLogic import GameLogic
import random

#note that this is now under some changes, so the class will fail right now

class Game:

    def __init__(self,player_one: Player, player_two: Player):
        self.player_one = player_one
        self.player_two = player_two
        #counting from 1 instead of the computer standard of zero
        self.round_counter = 1
        #this is for the ability where the player can keep a card
        self.player_one.cards_to_keep: List[Card]  = []
        self.player_two.cards_to_keep: List[Card] =  []
        self.active_weather_effect = set()

    #TRANSFER COMPLETED
    def determine_winner(self) -> str:

        #insert the winner here
        winner = GameLogic.determine_round_winner(self)


        return winner


    #TRANSFER COMPLETED
    def end_game_checker(self) -> str:

        winning_statement = GameLogic.end_game_checker(self)

        if winning_statement == "draw":
            print("A draw has taken place, nobody wins")
        elif winning_statement == "player one wins":
            print(f"{self.player_one.player_name} has won!")
        elif winning_statement == "player two wins":
            print(f"{self.player_two.player_name} has won!")

        return winning_statement

    #DON'T TRANSFER
    def determine_turn_order(self)-> None:

        p1_scoia = self.player_one.faction.lower().strip() == "scoia'tael"
        p2_scoia = self.player_two.factoin.lower().strip() == "scoia'tael"


        def coin_flip():
            coin_flip_var = random.randint(0, 1)
            if coin_flip_var == 0:
                self.player_one.turn_order_first = True
            else:
                self.player_two.turn_order_first = True


        #if they are both scoia'tael then just do a coin flip
        if p1_scoia and p2_scoia:
            coin_flip()

        elif p1_scoia and not p2_scoia:
            while True:
                player_choice = input("Player One (Scoia'tael): Do you want to go first or second? Note: type in first or second?")
                if player_choice.lower() == "first":
                    self.player_one.turn_order_first = True
                    break
                elif player_choice.lower() == "second":
                    self.player_two.turn_order_first = True
                    break
                else:
                    print("Please type in first or second")

        elif p2_scoia and not p1_scoia:
            while True:
                player_choice = input("Player Two (Scoia'tael): Do you want to go first or second")
                if player_choice.lower().strip() == "first":
                    self.player_one.turn_order_first = True
                    break
                elif player_choice.lower().strip() == "second":
                    self.player_two.turn_order_first = True
                    break
                else:
                    print("Please type in first or second")
        else:
            coin_flip()



    #This faction ability is going to cover northern realms and skilege
    #northern realms: keep a card after a win
    #skelllige: 2 random cards from the graveyard are placed on the battlefield at the start of the third round
    #monsters: keep random unit card out after each round

    #DID TRANSFER :
    def faction_ability(self, round_winner: str) -> None:

        GameLogic.faction_ability(self, round_winner)








    #DON'T COPY: BECAUSE THE GAMESTATE WILL SNAPSHOT THE GAME, NO NEED TO KEEP TRACK OF CARDS, GAMES JOB
    #this function will play the cards that are supposed to be kept on field or going to be brought back

    def play_card_to_keep(self) -> None:
        if self.player_one.cards_to_keep:
            for card in self.player_one.cards_to_keep:
                row = card.row_type
                self.player_one.board[row].append(card)
            self.player_one.cards_to_keep.clear()

        if self.player_two.cards_to_keep:
            for card in self.player_two.cards_to_keep:
                row = card.row_type
                self.player_two.board[row].append(card)
            self.player_two.cards_to_keep.clear()

    #Weather effect
    #will have to add to allow the ai to be able to simulate the next moves

    def check_weather_effect(self, weather_effect: str) -> None:
        if weather_effect in self.active_weather_effect:
            print(f"{weather_effect} is already in use")
            return

        self.active_weather_effect.add(weather_effect)

        def biting_frost(player: Player) -> None:
            for card in player.board["melee"]:
                if card.ability.lower().strip() != "hero":
                    card.current_strength = 1
            player.melee_row_weather_effect = True

        def impenetrable_fog(player: Player) -> None:
            for card in player.board["range"]:
                if card.ability.lower().strip() != "hero":
                    card.current_strength = 1
            player.range_row_weather_effect = True

        def torrential_rain(player) -> None:
            for card in player.board["siege"]:
                if card.ability.lower().strip() != "hero":
                    card.current_strength = 1
            player.siege_row_weather_effect = True

        def clear_weather(player: Player) -> None:
            # Clear all previous weather effects
            self.active_weather_effect.clear()

            # Restore strengths for all rows based on horn flags
            if player.melee_row_weather_effect:
                for card in player.board["melee"]:
                    card.current_strength = card.base_strength * (2 if player.melee_row_horn_effect else 1)

            if player.range_row_weather_effect:
                for card in player.board["range"]:
                    card.current_strength = card.base_strength * (2 if player.range_row_horn_effect else 1)

            if player.siege_row_weather_effect:
                for card in player.board["siege"]:
                    card.current_strength = card.base_strength * (2 if player.siege_row_horn_effect else 1)

            # Reset weather flags
            player.melee_row_weather_effect = False
            player.range_row_weather_effect = False
            player.siege_row_weather_effect = False

        # Now apply the correct weather effect
        weather_effect = weather_effect.lower().strip()

        if weather_effect == "biting frost":
            biting_frost(self.player_one)
            biting_frost(self.player_two)

        elif weather_effect == "impenetrable fog":
            impenetrable_fog(self.player_one)
            impenetrable_fog(self.player_two)

        elif weather_effect == "torrential rain":
            torrential_rain(self.player_one)
            torrential_rain(self.player_two)

        elif weather_effect == "skellige storm":
            if "torrential rain" in self.active_weather_effect and "impenetrable fog" in self.active_weather_effect:
                return
            elif "torrential rain" in self.active_weather_effect:
                impenetrable_fog(self.player_one)
                impenetrable_fog(self.player_two)
            elif "impenetrable fog" in self.active_weather_effect:
                torrential_rain(self.player_one)
                torrential_rain(self.player_two)

        elif weather_effect == "clear weather":
            if self.active_weather_effect:
                clear_weather(self.player_one)
                clear_weather(self.player_two)
            else:
                print("There is no weather effect to clear")

    #DON'T NEED TO COPY THIS: JUST FOR PLAYER
    def round_summary(self) -> None:
        print("Player one stats:")
        print(f"Sum: {self.player_one.sum} ")
        print("Player two stats:")
        print(f"Sum: {self.player_two.sum}")
        print("Round:")
        print(f"{self.round_counter}")

    #DON'T NEED TO COPY THIS: JUST FOR PLAYER
    def display_board(self) -> None:
        print("\n ===== BOARD =====")

        #change the player statement so that it prints out the right player
        def print_player_board(player: Player):
            print(f"---- {player.player_name.capitalize()} ----")
            for row in ["melee", "range", "siege"]:
                cards = player.board.get(row, [])
                card_names = [card.card_name for card in cards]
                print(f"{row.capitalize():<10}: {','.join(card_names) if card_names else 'Empty'}")
            #just adding a space between the two player boards
            print()
            print()

        print_player_board(self.player_one)
        print_player_board(self.player_two)

    #TRANSFERRED
    def use_card_ability(self, player: Player, og_card: Card) -> None:
        GameLogic.use_card_ability(self, player, og_card)



    #ignore previous, will need this class over on game logic so I can update child classes
    #transferred
    def maintain_effect(self, player: Player, card: Card) -> None:

        #both case
        if card.row == "melee" and player.melee_row_weather_effect and player.melee_row_horn_effect:
            card.current_strength = 2
        elif card.row == "range" and player.range_row_weather_effect and player.range_row_horn_effect:
            card.current_strength = 2
        elif card.row == "siege" and player.siege_row_weather_effect and player.siege_row_horn_effect:
            card.current_strength = 2
        else:
            #weather case
            if card.row == "melee" and player.melee_row_weather_effect:
                card.current_strength = 1
            elif card.row == "range" and player.range_row_weather_effect:
                card.current_strength = 1
            elif card.row == "siege" and player.siege_row_weather_effect:
                card.current_strength = 1

            #horn case
            if card.row == "melee" and player.melee_row_horn_effect:
                card.current_strength = card.base_strength * 2
            elif card.row == "range" and player.range_row_horn_effect:
                card.current_strength = card.base_strength * 2
            elif card.row == "siege" and player.siege_row_horn_effect:
                card.current_strength = card.base_strength * 2


        #morale booster case
        #going to not break from the for loop since morale boost can be stacked on top of the row over and over again

        for other_card in player.board[card.row]:
            if other_card.ability.lower().strip() == "morale boost":
                card.current_strength += 1

    #TRANSFERRED
    def check_buff(self, player: Player, og_card: Card) -> None:

        opponent = None

        if player == self.player_one:
            opponent = self.player_two
        else:
            opponent = self.player_one

        #this inner function go alongside the scorch
        #just to cancel any effects that would happen alongside it
        def cancel_effects_before_destroy(card: Card, player: Player):

            #morale boost case
            if card.ability == "morale boost":
                for other_card in player.board[card.row]:
                    other_card.current_strength = card.base_strength

            elif card.ability == "tight bond":

                tight_bond_count = []
                for other_card in player.board[card.row]:
                    if card == other_card:
                        tight_bond_count.append(card)


                #just pop one out to represent losing one card due to it being destroyed

                tight_bond_count.pop()


                for tight_bond_cards in tight_bond_count:
                    tight_bond_cards.current_strength *= tight_bond_cards.base_strength * len(tight_bond_count)





        if og_card.ability.lower().strip() == "scorch":

            max_strength_card = None
            max_strength_of_card = 0
            max_strength_card_player = None

            #first trying to find the largest strength card in the first player board

            for row in ["melee", "range", "siege"]:
                for card in player.board[row]:
                    if max_strength_of_card < card.current_strength:
                        max_strength_card = card
                        max_strength_of_card = card.current_strength
                        max_strength_card_player = player



            for row in ["melee", "range", "siege"]:
                for card in opponent.board[row]:
                    if max_strength_of_card < card.current_strength:
                        max_strength_card = card
                        max_strength_of_card = card.current_strength
                        max_strength_card_player = opponent

            #now we are going to go through and delete those card that are equal to it
            #then we delete that card that we are originating from

            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(player.board[row]):
                    if max_strength_of_card == card.current_strength:
                        cancel_effects_before_destroy(card, player)
                        player.graveyard.append(card)
                        del player.board[row][i]

            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(opponent.board[row]):
                    if max_strength_of_card == card.current_strength:
                        cancel_effects_before_destroy(card, opponent)
                        opponent.graveyard.append(card)
                        del opponent.board[row][i]


            #now we are going to delete the original max card

            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(max_strength_card_player.board[row]):
                    if card == max_strength_card:

                        cancel_effects_before_destroy(max_strength_card, max_strength_card_player)

                        max_strength_card_player.graveyard.append(max_strength_card)

                        del max_strength_card_player.board[row][i]





        elif og_card.ability.lower().strip() == "horn":

            while True:
                chosen_row = input("What row do you want to double?")
                if chosen_row == "melee":

                    for card in player.board["melee"]:
                        card.current_strength = card.base_strength * 2

                    player.melee_row_horn_effect = True

                elif chosen_row == "range":

                    for card in player.board["range"]:
                        card.current_strength = card.base_strength * 2

                    player.range_row_horn_effect = True

                elif chosen_row == "siege":
                    for card in player.board["siege"]:

                        card.current_strength = card.base_strength * 2

                    player.siege_row_horn_effect = True


                print("Please type in either melee, range, or siege please")


    #DON'T COPIED
    #BOARD BASED ABILITY
    def cancel_effects(self,player: Player,card: Card) -> None:
        if card.ability.lower().strip() == "tight bond":
            # Revert tight bond effect on other matching cards
            for row in ["melee", "range", "siege"]:
                for other_card in player.board[row]:
                    if other_card == card:
                        other_card.strength = other_card.base_strength
        elif card.ability.lower().strip() == "morale boost":
            # Remove the +1 morale boost from same-row cards
            for other_card in player.board[card.row]:
                if other_card is not card:
                    other_card.current_strength = other_card.base_strength



    #TRANSFERRED
    def calculate_strength(self, player: Player) -> None:
        GameLogic.calculate_strength_logic(player)




    #have to add a leader ability now
    #probably just going to add 5 because I don't want to add all the variants into the deck
    #1)Northern Realms: Foltest - Lord commander of the North - Clear Weather effects
    #2)Monsters: Eredin - The Treacherous - Double the strength of the vampires
    #3)Nilfgaard: Emhyr var Emreis - The white Flame - Look at opponent's hand
    #4)Scoia'tael: Francesca Findabair - QUeen of Dol Blathanna - Play a random card from your deck
    #5)Skillege: Crach an Craite - Shuffle all cards from each player graveyards back into their decks

    #TRANSFERRED
    def use_leader_ability(self, player: Player) -> None:
        GameLogic.use_leader_ability_logic(self, player)


    #DON'T COPY: FOR THE GAME TO FIX  THE ROUND AFTER EVERYTHING IS COMPLETED
    def round_resolve(self) -> None:
        self.player_one.round_end()
        self.player_two.round_end()

        self.check_weather_effect("clear weather")
        #need to effect the player
        for player in (self.player_one, self.player_two):
            for row in player.board.values():
                for card in row:
                    self.cancel_effects(player, card)

        self.calculate_strength(self.player_one)
        self.calculate_strength(self.player_two)

        if self.player_one.turn_order_first:
            self.player_one.turn_order_first = False
            self.player_two.turn_order_first = True
        else:
            self.player_two.turn_order_first = False
            self.player_one.turn_order_first = True
        self.round_counter += 1

    #DON'T NEED TO COPY
    #PLAYER FEATURE
    def display_player_hand(self, player: Player) -> None:
        for card in player.hand:
            print(card.card_name + " " + str(card.current_strength))


    #DON'T NEED TO COPY
    #AI SHOULDN'T BE CALCULATING EVERY DRAW CHANCE
    def player_starting_draw(self) -> None:

        #only going to draw 5 cards because I wanted to shorten hands to make the game better
        def redraw_mechanic(player: Player):
            if len(player.deck.cards) < 5:
                print(f"{player.player_name}Your deck isn't big enough to draw, please create a bigger deck")
                return

            # going to draw 10
            for _ in range(5):
                player.draw_card_to_hand()

            self.display_player_hand(player)

            # redraw logic
            print("One at a time you will be able to redraw 3 cards")
            redraw_choice = input("Please press enter if you want to redraw nothing though")

            if redraw_choice == "":
                print("Redrawing nothing")
                return


            redraws_remaining = 3
            while redraws_remaining > 0:
                redraw_card_choice = input(
                    "Please enter in the name of the card to redraw or press enter to skip").lower().strip()

                #if players want to skip one of their redraw choice
                if redraw_card_choice == "":
                    redraws_remaining -= 1
                    print(f"You have this many redraw remaining {redraws_remaining}")
                    continue

                for i, card in enumerate(player.hand):
                    if card.card_name.lower() == redraw_card_choice:

                        # want to reintroduce the card into the deck, then reshuffle that deck
                        player.deck.add_to_deck(player.hand.pop(i))
                        player.deck.shuffle()

                        new_card = player.deck.draw_from_deck()

                        if new_card:
                            player.hand.append(new_card)
                            print(f"You got rid of{redraw_card_choice}")
                            print(f"You now get {new_card.card_name}")
                        else:
                            print("Deck is empty. Could not draw a new card")
                        redraws_remaining -= 1
                        break

                print("Card isn't in your hand, could you please try again")



        #shuffle decks beforehand just to make sure
        self.player_one.deck.shuffle()
        self.player_two.deck.shuffle()


        redraw_mechanic(self.player_one)
        redraw_mechanic(self.player_two)










































































