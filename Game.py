from General_Game_Space import Player
import random

class Game:

    def __init__(self,player_one, player_two, player_one_name, player_two_name):
        self.player_one = player_one
        self.player_two = player_two
        self.player_one_name = player_one_name
        self.player_two_name = player_two_name
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
        if self.player_one.lives == 0 and self.player_two.lives == 0:
            if self.player_one.faction != "nilfgaard" and self.player_two.faction != "nilfgaard":
                print("A draw has taken place, nobody wins")
                return "draw"
            elif self.player_one.faction == "nilfgaard" and self.player_two.faction != "nilfgaard":
                print("Player one has activated its ability and player two has lost")
                return "player one wins"
            elif self.player_one.faction != "nilfgaard" and self.player_two.faction == "nilfgaard":
                print("Player two has activated its ability and player one has lost")
                return "player two wins"
        elif self.player_one.lives == 0:
            print("Player two has won!")
            return "player two wins"
        elif self.player_two.lives == 0:
            print("Player one has won!")
            return "player one wins"

    def determine_turn_order(self):
        if self.player_one.faction == "scoia'tael":
            player_choice_loop = True
            while player_choice_loop:
                player_choice = input("Player One (Scoia'tael): Do you want to go first or second? Note: type in first or second?")
                if player_choice.lower() == "first":
                    self.player_one.turn_order_first = True
                    player_choice_loop = False
                elif player_choice.lower() == "second":
                    self.player_two.turn_order_first = True
                    player_choice_loop = False
        elif self.player_two.faction == "scoia'tael":
            player_choice_loop = True
            while player_choice_loop:
                player_choice = input("Player Two (Scoia'tael): Do you want to go first or second")
                if player_choice.lower() == "first":
                    self.player_one.turn_order_first = True
                    player_choice_loop = False
                elif player_choice.lower() == "second":
                    self.player_two.turn_order_first = True
                    player_choice_loop = False
        else:
            coin_flip = random.randint(0,1)
            if coin_flip == 0:
                self.player_one.turn_order_first = True
            else:
                self.player_two.turn_order_first = True


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

        def print_player_board(player, name):
            print("---- Player One ----")
            for row in ["melee", "range", "siege"]:
                cards = player.board.get(row, [])
                card_names = [card.card_name for card in cards]
                print(f"{row.capitalize():<10}: {','.join(card_names) if card_names else 'Empty'}")

        print_player_board(self.player_one, self.player_one_name)
        print_player_board(self.player_two, self.player_two_name)

    def use_card_ability(self, player, og_card):
        #gathering the card's ability
        if player == self.player_one:

            if og_card.ability == "tight bond":
                for row in ["melee", "range", "siege"]:
                    for card in self.player_one.board[row]:
                        if og_card.ability == "tight bond" and og_card.ability == card.ability and og_card.card_name == card.card_name and og_card.row == card.row:
                            card.strength *= 2
                            og_card.strength *= 2

            elif og_card.ability == "medic":
                if self.player_one.graveyard is None:
                    print("There is no cards to heal")
                else:
                    for card in self.player_one.graveyard:
                        print(card.card_name)
                    card_choice = input("So what card do you want?")
                    for i, c in enumerate(self.player_one.graveyard):
                        if c.card_name == card_choice and c.card_type == "unit" and c.ability != "hero":
                            row = c.row
                            self.player_one.board[row].append(c)
                            self.player_one.strength += c.strength
                            del self.player_one.graveyard[i]
                            break

            elif og_card.ability == "munster":
                for i, card in enumerate(self.player_one.deck):
                        if og_card.card_name == card.card_name:
                            self.player_one.strength += card.strength
                            self.player_one.board[card.row].append(card)
                            # we are using del so that we delete the specific index and not deleting all the cards with the same name
                            del self.player_one.deck[i]

            elif og_card.ability == "morale boost":
                for card in self.player_one.board[og_card.row]:
                    if og_card.card_name != card.card_name:
                        card.strength += 1

            elif og_card.ability == "spy":
                self.player_two.board[og_card.row].append(og_card)
                for _ in range(2):
                    self.player_one.deck.draw_from_deck()

            elif og_card.ability == "decoy":
                for row in ["melee", "range", "siege"]:
                    for card in self.player_one.board[row]:
                        print(card.card_name)
                card_chosen = input("What card do you want?")
                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_one.board[row]):
                        if card.card_name == card_chosen:
                            self.player_one.hand.append(card)
                            self.player_one.board[row][i] = og_card
                            return

            elif og_card.ability == "scorch":
                max_strength_player_one = 0
                max_card_player_one = None
                for row in ["melee", "range", "siege"]:
                    for card in self.player_one.board[row]:
                        if max_strength_player_one < card.strength and card.ability != "hero":
                            max_card_player_one = card
                            max_strength_card_player_one = card.strength

                max_card_player_two = None
                max_strength_player_two = 0
                for row in ["melee", "range", "siege"]:
                    for card in self.player_two.board[row]:
                        if max_strength_player_two < card.strength and card.ability != "hero":
                            max_card_player_two = card
                            max_strength_player_two = card.strength

                #now we are deleting it
                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_one.board[row]):
                        if card is max_card_player_one:
                            del self.player_one.board[row][i]
                            break

                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_two.board[row]):
                        if card is max_card_player_two:
                            del self.player_two.board[row][i]
                            break

        elif player == self.player_two:

            if og_card.ability == "tight bond":
                for row in ["melee", "range", "siege"]:
                    for card in self.player_two.board[row]:
                        if og_card.ability == "tight bond" and og_card.ability == card.ability and og_card.card_name == card.card_name and og_card.row == card.row:
                            card.strength *= 2
                            og_card.strength *= 2

            elif og_card.ability == "medic":
                if self.player_two.graveyard is None:
                    print("There is no cards to heal")
                else:
                    for card in self.player_two.graveyard:
                        print(card.card_name)
                    card_choice = input("So what card do you want?")
                    for i, c in enumerate(self.player_two.graveyard):
                        if c.card_name == card_choice and c.card_type == "unit" and c.ability != "hero":
                            row = c.row
                            self.player_two.board[row].append(c)
                            self.player_two.strength += c.strength
                            del self.player_two.graveyard[i]
                            break

            elif og_card.ability == "munster":
                for i, card in enumerate(self.player_two.deck):
                        if og_card.card_name == card.card_name:
                            self.player_two.strength += card.strength
                            self.player_two.board[card.row].append(card)
                            # we are using del so that we delete the specific index and not deleting all the cards with the same name
                            del self.player_two.deck[i]

            elif og_card.ability == "morale boost":
                for card in self.player_two.board[og_card.row]:
                    if og_card.card_name != card.card_name:
                        card.strength += 1

            elif og_card.ability == "spy":
                self.player_one.board[og_card.row].append(og_card)
                for _ in range(2):
                    self.player_two.deck.draw_from_deck()

            elif og_card.ability == "decoy":
                for row in ["melee", "range", "siege"]:
                    for card in self.player_two.board[row]:
                        print(card.card_name)
                card_chosen = input("What card do you want?")
                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_two.board[row]):
                        if card.card_name == card_chosen:
                            self.player_two.hand.append(card)
                            self.player_two.board[row][i] = og_card
                            return

            elif og_card.ability == "scorch":
                max_strength_player_one = 0
                max_card_player_one = None
                for row in ["melee", "range", "siege"]:
                    for card in self.player_one.board[row]:
                        if max_strength_player_one < card.strength and card.ability != "hero":
                            max_card_player_one = card
                            max_strength_card_player_one = card.strength

                max_card_player_two = None
                max_strength_player_two = 0
                for row in ["melee", "range", "siege"]:
                    for card in self.player_two.board[row]:
                        if max_strength_player_two < card.strength and card.ability != "hero":
                            max_card_player_two = card
                            max_strength_player_two = card.strength

                #now we are deleting it
                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_one.board[row]):
                        if card is max_card_player_one:
                            del self.player_one.board[row][i]
                            break

                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(self.player_two.board[row]):
                        if card is max_card_player_two:
                            del self.player_two.board[row][i]
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
