from General_Game_Space import Player
import random

class Game:

    def __init__(self,player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        #we need to check the counter because of Skillege ability
        self.round_counter = 0
        #this is for the ability where the player can keep a card
        self.player_one.cards_to_keep  = []
        self.player_two.cards_to_keep =  []
        self.player_one_sum = 0
        self.player_two_sum = 0
        self.player_one_weather_sum = 0
        self.player_two_weather_sum = 0
        self.active_weather_effect = set()

    def determine_winner(self):
        #An outright win case
        if self.player_one.strength > self.player_two.strength:
            self.player_two.lose_life()
            print("Player one has won the round")
            return "player one wins"
        elif self.player_two.strength > self.player_one.strength:
            self.player_one.lose_life()
            print("Player two has one the round")
            return "player two wins"
        #Tie cases
        elif self.player_one.strength == self.player_two.strength:
            self.player_one.lose_life()
            self.player_two.lose_life()
            return "draw"



    def end_game_checker(self):
        p1_nilfgaard = self.player_one.faction.lower() == "nilfgaard"
        p2_nilfgaard = self.player_two.faction.lower() == "nilfgaard"

        if self.player_one.lives == 0 and self.player_two.lives == 0:
            if not p1_nilfgaard and not p2_nilfgaard:
                print("A draw has taken place, nobody wins")
                return "draw"
            elif p1_nilfgaard and not p2_nilfgaard:
                print("Player one has activated its ability and player two has lost")
                return "player one wins"
            elif not p1_nilfgaard and p2_nilfgaard:
                print("Player two has activated its ability and player one has lost")
                return "player two wins"
        elif self.player_one.lives == 0:
            print("Player two has won!")
            return "player two wins"
        elif self.player_two.lives == 0:
            print("Player one has won!")
            return "player one wins"

    #refactor this to just have more readable code
    def determine_turn_order(self):

        p1_scoia = self.player_one.faction.lower() == "scoia'tael"
        p2_scoia = self.player_two.faction.lower() == "scoia'tael"


        def coin_flip():
            coin_flip_var = random.randint(0, 1)
            if coin_flip_var == 0:
                self.player_one.turn_order_first = True
            else:
                self.player_two.turn_order_first = True

        #both scoia'tael case:
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
                if player_choice.lower() == "first":
                    self.player_one.turn_order_first = True
                    break
                elif player_choice.lower() == "second":
                    self.player_two.turn_order_first = True
                    break
                else:
                    print("Please type in first or second")
        else:
            coin_flip()


    def round_resolve(self):
        self.player_one.round_end()
        self.player_two.round_end()
        if self.player_one.turn_order_first == True:
            self.player_one.turn_order_first = False
            self.player_two.turn_order_first = True
        else:
            self.player_two.turn_order_first = False
            self.player_one.turn_order_first = True
        self.round_counter += 1

    #This faction ability is going to cover northern realms and skilege
    def faction_ability(self, round_winner, round_count):
        # monster faction case:
        # ability: keeps random unit card out after each round

        #maybe add functions to make the logic more clear and the code less repetitive
        #1)Random draw code
        #2)??

        if self.player_one.faction == "monsters" and self.player_two.faction == "monsters":
            player_one_board = self.player_one.board
            player_two_board = self.player_two.board

            player_one_valid_rows = [row for row in player_one_board if player_one_board[row]]
            player_two_valid_rows = [row for row in player_two_board if player_two_board[row]]

            if player_one_valid_rows:
                chosen_row = random.choice(player_one_valid_rows)
                card_to_keep = random.choice(player_one_board[chosen_row])

                # Add the card to the keep list
                self.player_one.cards_to_keep.append(card_to_keep)

            if player_two_valid_rows:
                chosen_row = random.choice(player_two_valid_rows)
                card_to_keep = random.choice(player_two_board[chosen_row])

                # Add the card to the keep list
                self.player_two.cards_to_keep.append(card_to_keep)

        elif self.player_one.faction == "monsters":
            board = self.player_one.board
            valid_rows = [row for row in board if board[row]]

            if valid_rows:
                chosen_row = random.choice(valid_rows)
                card_to_keep = random.choice(board[chosen_row])

                # Add the card to the keep list
                self.player_one.cards_to_keep.append(card_to_keep)

                print(f"(Player One): The monsters faction keeps card '{card_to_keep.card_name}' on the board.")
        elif self.player_two.faction == "monsters":
            board = self.player_two.board
            valid_rows = [row for row in board if board[row]]

            if valid_rows:
                chosen_row = random.choice(valid_rows)
                card_to_keep = random.choice(board[chosen_row])

                # Add the card to the keep list
                self.player_two.cards_to_keep.append(card_to_keep)

                print(f"(Player Two): The monsters faction keeps the card '{card_to_keep.card_name}' on the board")

        if self.player_one.faction == "northern realms" and round_winner == "player one wins":
            extra_card_player_one = self.player_one.deck.draw_from_deck()
            self.player_one.hand.append(extra_card_player_one)

            print(f"(Player One): Northern Realms faction draws a card '{extra_card_player_one.card_name}'")
        elif self.player_two.faction == "northern realms" and round_winner == "player two wins":
            extra_card_player_two = self.player_two.deck.draw_from_deck()
            self.player_two.hand.append(extra_card_player_two)

            print(f"(Player Two): Northern Realms faction draws a card '{extra_card_player_two.card_name}'")

        #Note in the future, get rid of the remove as it will remove duplicates wihtin the graveyard which is terrible
        if self.player_one.faction == "skellige" and self.player_two.faction == "skellige" and round_count == 3:
            for _ in range(2):
                card_to_keep = random.choice(self.player_one.graveyard)
                self.player_one.cards_to_keep.append(card_to_keep)
                for i, c in enumerate(self.player_one.graveyard):
                    if c is card_to_keep:
                        del self.player_one.graveyard[i]
                        break
            for _ in range(2):
                card_to_keep = random.choice(self.player_two.graveyard)
                self.player_two.cards_to_keep.append(card_to_keep)
                for i, c in enumerate(self.player_two.graveyard):
                    if c is card_to_keep:
                        del self.player_two.graveyard[i]
                        break
        elif self.player_one.faction == "skellige" and round_count == 3:
            for _ in range(2):
                card_to_keep = random.choice(self.player_one.graveyard)
                self.player_one.cards_to_keep.append(card_to_keep)
                for i, c in enumerate(self.player_one.graveyard):
                    if c is card_to_keep:
                        del self.player_one.graveyard[i]
                        break
        elif self.player_two.faction == "skellige" and round_count == 3:
            for _ in range(2):
                card_to_keep = random.choice(self.player_two.graveyard)
                self.player_two.cards_to_keep.append(card_to_keep)
                for i, c in enumerate(self.player_two.graveyard):
                    if c is card_to_keep:
                        del self.player_two.graveyard[i]
                        break




    def play_card_to_keep(self):
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
    def check_weather_effect(self, weather_effect):
        if weather_effect in self.active_weather_effect:
            print(f"{weather_effect} is already in use")
            return

        self.active_weather_effect.add(weather_effect)

        if weather_effect == "biting frost":
            for card in self.player_one.board["melee"]:
                if card.ability != "hero":
                    self.player_one_weather_sum += (card.strength - 1)
            self.player_one_weather_sum *= -1
            self.player_one_sum += self.player_one_weather_sum

            for card in self.player_two.board["melee"]:
                if card.ability != "hero":
                    self.player_two_weather_sum += (card.strength - 1)
            self.player_two_weather_sum *= -1
            self.player_two_sum += self.player_two_weather_sum


        elif weather_effect == "impenetrable fog":
            for card in self.player_one.board["range"]:
                if card.ability != "hero":
                    self.player_one_weather_sum += (card.strength - 1)
            self.player_one_weather_sum *= -1
            self.player_one_sum += self.player_one_weather_sum

            for card in self.player_two.board["range"]:
                if card.ability != "hero":
                    self.player_two_weather_sum += (card.strength - 1)
            self.player_two_weather_sum *= -1
            self.player_two_sum += self.player_two_weather_sum

        elif weather_effect == "torrential rain":
            for card in self.player_one.board["siege"]:
                if card.ability != "hero":
                    self.player_one_weather_sum += (card.strength - 1)
            self.player_one_weather_sum *= -1
            self.player_one_sum += self.player_one_weather_sum

            for card in self.player_two.board["siege"]:
                if card.ability != "hero":
                    self.player_two_weather_sum += (card.strength - 1)
            self.player_two_weather_sum *= -1
            self.player_two_sum += self.player_two_weather_sum

        elif weather_effect == "skelliege storm":
            if "torrential rain" in self.active_weather_effect and "impenetrable fog" in self.active_weather_effect:
                return
            elif "torrential rain" in self.active_weather_effect:
                for card in self.player_one.board["range"]:
                    if card.ability != "hero":
                        self.player_one_weather_sum += (card.strength - 1)
                self.player_one_weather_sum *= -1
                self.player_one_sum += self.player_one_weather_sum

                for card in self.player_two.board["range"]:
                    if card.ability != "hero":
                        self.player_two_weather_sum += (card.strength - 1)
                self.player_two_weather_sum *= -1
                self.player_two_sum += self.player_two_weather_sum
            elif "impenetrable fog" in self.active_weather_effect:
                for card in self.player_one.board["siege"]:
                    if card.ability != "hero":
                        self.player_one_weather_sum += (card.strength - 1)
                self.player_one_weather_sum *= -1
                self.player_one_sum += self.player_one_weather_sum

                for card in self.player_two.board["siege"]:
                    if card.ability != "hero":
                        self.player_two_weather_sum += (card.strength - 1)
                self.player_two_weather_sum *= -1
                self.player_two_sum += self.player_two_weather_sum

        elif weather_effect == "clear weather":
            self.active_weather_effect.clear()
            self.player_one_weather_sum *= -1
            self.player_two_weather_sum *= -1
            self.player_one_sum += self.player_one_weather_sum
            self.player_two_sum += self.player_two_weather_sum

    #Maybe I will just to get rid of the reliance on the other systems
    def round_summary(self):
        print("Player one stats:")
        print(f"Sum: {self.player_one_sum} ")
        print("Player two stats:")
        print(f"Sum: {self.player_two_sum}")
        print("Round:")
        print(f"{self.round_counter}")

    def display_board(self):
        print("\n ===== BOARD =====")

        #change the player statement so that it prints out the right player
        def print_player_board(player):
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


    def use_card_ability(self, player, og_card):
        opponent = None

        if player == self.player_one:
            opponent = self.player_two
        else:
            opponent = self.player_one

        if og_card.ability == "tight bond":
            for row in ["melee", "range", "siege"]:
                for card in player.board[row]:
                    if og_card.ability == "tight bond" and og_card.ability == card.ability and og_card.card_name == card.card_name and og_card.row == card.row:
                        card.strength *= 2
                        og_card.strength *= 2

        elif og_card.ability == "medic":
            if player.graveyard is None:
                print("There is no cards to heal")
            else:
                for card in player.graveyard:
                    print(card.card_name)
                card_choice = input("So what card do you want?")
                for i, c in enumerate(player.graveyard):
                    if c.card_name == card_choice and c.card_type == "unit" and c.ability != "hero":
                        row = c.row
                        player.board[row].append(c)
                        player.strength += c.strength
                        del player.graveyard[i]
                        break

        elif og_card.ability == "munster":
            for i, card in enumerate(player.deck):
                    if og_card.card_name == card.card_name:
                        player.strength += card.strength
                        player.board[card.row].append(card)
                        # we are using del so that we delete the specific index and not deleting all the cards with the same name
                        del player.deck[i]

        elif og_card.ability == "morale boost":
            for card in player.board[og_card.row]:
                if og_card.card_name != card.card_name:
                    card.strength += 1

        elif og_card.ability == "spy":
            opponent[og_card.row].append(og_card)
            for _ in range(2):
                player.deck.draw_from_deck()

        elif og_card.ability == "decoy":
            for row in ["melee", "range", "siege"]:
                for card in player.board[row]:
                    print(card.card_name)
            card_chosen = input("What card do you want?")
            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(player.board[row]):
                    if card.card_name == card_chosen:
                        player.hand.append(card)
                        player.board[row][i] = og_card
                        return

        elif og_card.ability == "scorch":
            max_strength_player_one = 0
            max_card_player_one = None
            for row in ["melee", "range", "siege"]:
                for card in player.board[row]:
                    if max_strength_player_one < card.strength and card.ability != "hero":
                        max_card_player_one = card
                        max_strength_card_player_one = card.strength

            max_card_player_two = None
            max_strength_player_two = 0
            for row in ["melee", "range", "siege"]:
                for card in opponent[row]:
                    if max_strength_player_two < card.strength and card.ability != "hero":
                        max_card_player_two = card
                        max_strength_player_two = card.strength

                #now we are deleting it
            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(player.board[row]):
                    if card is max_card_player_one:
                        del player.board[row][i]
                        break

            for row in ["melee", "range", "siege"]:
                for i, card in enumerate(player.board[row]):
                    if card is max_card_player_two:
                        del player.board[row][i]
                        break


    def cancel_effects(self,player,card):
        if card.ability == "tight bond":
            # Revert tight bond effect on other matching cards
            for row in ["melee", "range", "siege"]:
                for other_card in player.board[row]:
                    if (other_card.ability == "tight bond" and
                            other_card.card_name == card.card_name and
                            other_card.row == card.row):
                        other_card.strength //= 2  # Undo the doubling
        elif card.ability == "morale boost":
            # Remove the +1 morale boost from same-row cards
            for other_card in player.board[card.row]:
                if other_card is not card:
                    other_card.strength -= 1



    #Debugging function
    def calculate_strength(self, player):
        total = 0
        for row in ["melee", "range", "siege"]:
            for card in player.board[row]:
                total += card.strength
        player.strength = total












