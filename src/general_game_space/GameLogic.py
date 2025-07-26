from src.ai.PlayerState import PlayerState
from src.general_game_space import Game, Player
from src.cards.Card import Card
from typing import Union, Optional
from random import random


#creating this class so that we can have pure functions here that don't rely on printing information so that both the AI class and this regular game class can use it

#okay, for today we are just simplifying the logic

class GameLogic:

    #ai needs to be able to determine the round winner
    @staticmethod
    def determine_round_winner(game_or_gamestate: Union[Game, "GameState"]) -> str:

        def determining_winner_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player,PlayerState]) -> str:
            if player_one.sum > player_two.sum:
                player_two.lose_life()
                return "player one wins"
            elif player_two.sum > player_one.sum:
                player_one.lose_life()
                return "player two wins"
            # Tie cases
            elif player_one.sum == player_two.sum:
                player_one.lose_life()
                player_two.lose_life()
                return "draw"


        if isinstance(game_or_gamestate, Game):
            determining_winner_player_input(game_or_gamestate.player_one, game_or_gamestate.player_two)
        elif isinstance(game_or_gamestate, "GameState"):
            determining_winner_player_input(game_or_gamestate.ai_player_state, game_or_gamestate.opponent_state)
        else:
            raise ValueError("Must input either a Game or GameState class")



    #note that we need the card and the player card
    #ai should be able to understand how the ai is able to use a card ability

    @staticmethod
    def use_card_ability(game_or_game_state: Union[Game, "GameState"], player: Union[Player,  PlayerState], og_card) -> None:

        #use the player ability input:
        def use_card_ability_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player,PlayerState]) -> None:

            #first the opponent should be set 0

            opponent = None

            #setting the players
            if player == player_one:
                opponent = player_two
            else:
                opponent = player_one

            #going to change the implementation of the tight bond ability
            if og_card.ability.lower().strip() == "tight bond":
                # a list for holding all the tight bond cards
                # because the calculation is not doubling
                # it is the original strength * number of cards
                tight_bond_cards = []


                for row in ["melee", "range", "siege"]:
                    for card in player.board[row]:
                        if og_card == card:
                            tight_bond_cards.append(card)


                for card in tight_bond_cards:
                    card.current_strength = card.base_strength * len(tight_bond_cards)

            #bring back card from the graveyard
            elif og_card.ability.lower().strip() == "medic":
                #if there was no graveyard
                if not player.graveyard:
                    print("There is no cards to heal")
                else:
                    #for card in the graveyards
                    for card in player.graveyard:
                        print(card.card_name)
                    card_choice = input("So what card do you want?")
                    for i, c in enumerate(player.graveyard):
                        if c.card_name == card_choice and c.card_type == "unit" and c.ability != "hero":
                            row = c.row
                            player.board[row].append(c)
                            del player.graveyard[i]
                            break

            #delete specific index
            elif og_card.ability.lower().strip() == "muster":
                for i, card in enumerate(player.deck):
                        if og_card == card:
                            player.board[card.row].append(card)
                            # we are using del so that we delete the specific index and not deleting all the cards with the same name
                            del player.deck[i]

            #morale booster
            elif og_card.ability.lower().strip() == "morale boost":
                for card in player.board[og_card.row]:
                    if og_card.card_name != card.card_name:
                        card.current_strength += 1

            #the spy
            elif og_card.ability.lower().strip() == "spy":
                #spy's go on opponent's board
                opponent.board[og_card.row].append(og_card)
                for _ in range(2):
                    card = player.deck.draw_from_deck()
                    if card:
                        player.hand.append(card)

            #decoy
            elif og_card.ability.lower().strip() == "decoy":
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


            if isinstance(game_or_game_state, Game):
                use_card_ability_player_input(game_or_game_state.player_one, game_or_game_state.player_two)
            elif isinstance(game_or_game_state, "GameState"):
                use_card_ability_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)
            else:
                raise ValueError("Must input either a Game or GameState class")

    #ai should know how to end the game and how to check that case, also to use nilfgaardian case to it advantage
    @staticmethod
    def end_game_checker(game_or_game_state: Union[Game, "GameState"]) -> str:

        def end_game_checker_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player,PlayerState]) -> str:

            #setting the nilfgaardian equal the nilfgaardian
            p1_nilfgaardian = player_one.faction.lower() == "nilfgaardian"
            p2_nilfgaardian = player_two.faction.lower() == "nilfgaardian"

            # using <= just to make sure if a glitch happens and something became negative that it would error check for that.
            if player_one.lives <= 0 and player_two.lives <= 0:

                if not p1_nilfgaardian and not p2_nilfgaardian:
                    return "draw"

                elif p1_nilfgaardian and not p2_nilfgaardian:
                    return "player one wins"

                elif not p1_nilfgaardian and p2_nilfgaardian:
                    return "player two wins"

            elif player_one.lives <= 0:
                return "player two wins"

            elif player_two.lives <= 0:
                return "player one wins"

        if isinstance(game_or_game_state, Game):
            end_game_checker_player_input(game_or_game_state.player_one, game_or_game_state.player_two)

        elif isinstance(game_or_game_state, "GameState"):
            end_game_checker_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)

        else:
            raise ValueError("Must input either a Game or GameState class")


    #no need to change the logic here
    @staticmethod
    def calculate_strength_logic(player: Union[Player, PlayerState]) -> None:

        total = 0

        for row in ["melee", "range", "siege"]:
            for card in player.board[row]:
                total += card.current_strength

        player.sum = total

    #ai needs to be able to use its' own leader ability
    @staticmethod
    def use_leader_ability_logic(game_or_game_state, player: Union[Player, PlayerState] ) -> None:

        def use_leader_ability_logic_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player, PlayerState]) -> str:

            #Opponent = None
            opponent = None

            #setting players
            if player == player_one:
                opponent = player_two
            else:
                opponent = player_one

            #returning function here, might make a function that if the ai get's this back it knows that the leader_used has already been used as an edge case check
            if player.leader_used:
                return "You have already used this ability"

            else:
                # basically using clear weather
                if player.leader_card.leader_ability.lower().strip() == "clear" and player.leader_card.faction.lower().strip() == "northern realms":

                    #setting the active weather effects
                    if game_or_game_state.active_weather_effects:
                        game_or_game_state.active_weather_effect.clear()
                        # doing it twice so we don't clear it twice
                        for row in ["melee", "range", "siege"]:
                            for card in player.board[row]:
                                if card.is_affected_by_weather and card.is_affected_by_horn:
                                    card.current_strength = card.base_strength * 2
                                elif card.is_affected_by_weather:
                                    card.current_strength = card.base_strength

                        for row in ["melee", "range", "siege"]:
                            for card in opponent.board[row]:
                                if card.is_affected_by_weather and card.is_affected_by_horn:
                                    card.current_strength = card.base_strength * 2
                                elif card.is_affected_by_weather:
                                    card.current_strength = card.base_strength

                    #the player here is being used
                    player.leader_used = True

                # looking at 3 cards in your opponents hand
                elif player.leader_card.leader_ability.lower().strip() == "look at opponent hand" and player.leader_card.faction.lower().strip() == "nilfgaardian":


                    if opponent.ai_player:
                        cards_to_show = random.sample(opponent.hand, min(3, len(opponent.hand)))
                        print("3 of the opponenets hand")
                        for card in cards_to_show:
                            print(card.card_name)
                    else:
                        cards_to_show = random.sample(opponent.hand, min(3, len(opponent.hand)))
                        for card in cards_to_show:
                            player.opponent_hand(card)

                    player.leader_used = True

                # boosting the strength by 3
                elif player.leader_card.leader_ability.lower().strip() == "double spy" and player.leader_card.faction.lower().strip() == "monsters":

                    for row in ["melee", "range", "siege"]:
                        for card in player .board[row]:
                            if card.ability == "spy":
                                card.current_strength *= 2

                    for row in ["melee", "range", "siege"]:
                        for card in opponent.player_two.board[row]:
                            if card.ability == "spy":
                                card.current_strength *= 2

                    player.leader_used = True

                # lets you play special card from your deck

                elif player.leader_card.leader_ability.lower().strip() == "play a random card" and player.leader_card.faction.lower().strip() == "scoia'tael":

                    for card in player.deck:
                        if card.card_type != " ":
                            chosen_card = random.choice(player.deck)
                            player.hand.append(chosen_card)
                            player.deck.remove(chosen_card)
                            print(f"{chosen_card}")

                    player.leader_used = True

                # shuffle all cards from each player's graveyard back into their decks
                elif player.leader_card.leader_ability.lower().strip() == "crach an craite" and player.leader_card.faction.lower().strip() == "skellige":

                    player.deck.extend(player.graveyard)
                    player.graveyard.clear()
                    random.shuffle(player.deck)

                    player.leader_used = True

        if isinstance(game_or_game_state, Game):
            use_leader_ability_logic_player_input(game_or_game_state.player_one, game_or_game_state.player_two)
        elif isinstance(game_or_game_state, "GameState"):
            use_leader_ability_logic_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)
        else:
            raise ValueError("Must input either a Game or GameState class")


    #need to change for AI version
    #need to change the player union
    @staticmethod
    def check_buff_logic(game_or_game_state: Union[Game, "GameState"], player: Union[Player, PlayerState], og_card: Card, selected_row: Optional[str] = None) -> None:
        #use the leader ability logic player input
        def check_buff_logic_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player, PlayerState]) -> None:

            # grabbing opponent = None

            opponent = None

            # setting the player_one
            if player == player_one:
                opponent = player_two
            else:
                opponent = player_one

            # this inner function go alongside the scorch
            # just to cancel any effects that would happen alongside it
            #this should be fine for the AI implementation
            def cancel_effects_before_destroy(card: Card, player: Player) -> None:
                # morale boost case
                if card.ability == "morale boost":
                    for other_card in player.board[card.row]:
                        other_card.current_strength = card.base_strength
                elif card.ability == "tight bond":

                    #
                    tight_bond_count = []
                    for other_card in player.board[card.row]:
                        if card == other_card:
                            tight_bond_count.append(card)

                    # just pop one out to represent losing one card due to it being destroyed

                    tight_bond_count.pop()

                    for tight_bond_cards in tight_bond_count:
                        tight_bond_cards.current_strength *= tight_bond_cards.base_strength * len(tight_bond_count)

            # in the works

            if og_card.ability.lower().strip() == "scorch":

                max_strength_card = None
                max_strength_of_card = 0
                max_strength_card_player = None

                # first trying to find the largest strength card in the first player board

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

                # now we are going to go through and delete those card that are equal to it
                # then we delete that card that we are originating from

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

                # now we are going to delete the original max card

                for row in ["melee", "range", "siege"]:
                    for i, card in enumerate(max_strength_card_player.board[row]):
                        if card == max_strength_card:
                            cancel_effects_before_destroy(max_strength_card, max_strength_card_player)

                            max_strength_card_player.graveyard.append(max_strength_card)

                            del max_strength_card_player.board[row][i]




            #need to create an Ai
            elif og_card.ability.lower().strip() == "horn":

                if not player.ai_player:

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

                        return "Please type in either melee, range, or siege please"


                #now the ai part here we need to discuss logic
                #the ai should put it towards the highest strength row?

                elif player.ai_player:

                    if selected_row == "melee":

                        for card in player.board["melee"]:
                            card.current_strength = card.base_strength * 2

                        player.melee_row_horn_effect = True

                    elif selected_row == "range":

                        for card in player.board["range"]:
                            card.current_strength = card.base_strength * 2

                        player.range_row_horn_effect = True

                    elif selected_row == "siege":
                        for card in player.board["siege"]:
                            card.current_strength = card.base_strength * 2

                        player.siege_row_horn_effect = True

            if isinstance(game_or_game_state, Game):
                check_buff_logic_player_input(game_or_game_state.player_one, game_or_game_state.player_two)
            elif isinstance(game_or_game_state, "GameState"):
                check_buff_logic_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)
            else:
                raise ValueError("Must input either a Game or GameState class")


    #the ai should know this as well
    @staticmethod
    def faction_ability_logic(game_or_game_state: Union[Game, "GameState"], round_winner: str ) -> None:

        def monster_keep_card(player, board) -> None:
            valid_rows = [row for row in board if board[row]]
            if valid_rows:
                chosen_row = random.choice(valid_rows)
                card_to_keep = random.choice(board[chosen_row])
                player.cards_to_keep.append(card_to_keep)

        def northern_realms_draw_card(player) -> None:
            extra_card_player = player.deck.draw_from_deck()
            player.hand.append(extra_card_player)

        def skellige_draw_from_graveyard(player) -> None:
            # not checking for two cards because you can't win a round by placing somehow less than two cards the whole game in total
            for _ in range(2):
                card_to_keep = random.choice(player.graveyard)
                player.cards_to_keep.append(card_to_keep)
                for i, c in enumerate(player.graveyard):
                    if c is card_to_keep:
                        del player.graveyard[i]
                        break

        def faction_ability_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player, PlayerState]) -> None:
            # monster's block
            if  player_one.faction.lower().strip() == "monsters" and player_two.faction.lower().strip() == "monsters":

                monster_keep_card(player_one, player_one.board)

                monster_keep_card(player_two, player_two.board)

            elif player_one.faction.lower().strip() == "monsters":
                monster_keep_card(player_one, player_one.board)

            elif player_two.faction.lower().strip() == "monsters":
                monster_keep_card(player_two, player_two.board)

            # northern realm's block
            if player_one.faction.lower().strip() == "northern realms" and round_winner.lower().strip() == "player one wins":

                northern_realms_draw_card(player_one)

            elif player_two.faction.lower().strip() == "northern realms" and round_winner.lower().strip() == "player two wins":

                northern_realms_draw_card(player_two)

            # skellige's block

            # only works on round 3
            if game_or_game_state.round_counter == 3:

                if player_one.faction.lower().strip() == "skellige" and player_two.faction.lower().strip() == "skellige":

                    skellige_draw_from_graveyard(player_one)

                    skellige_draw_from_graveyard(player_two)

                elif player_one.faction.lower().strip() == "skellige":

                    skellige_draw_from_graveyard(player_one)

                elif player_two.faction.lower().strip() == "skellige":

                    skellige_draw_from_graveyard(player_two)

        if isinstance(game_or_game_state, Game):
            faction_ability_player_input(game_or_game_state.player_one, game_or_game_state.player_two)
        elif isinstance(game_or_game_state, "GameState"):
            faction_ability_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)
        else:
            raise ValueError("Must input either a Game or GameState class")


    #coverting this into a lite method for the ai, just to handle the

    @staticmethod
    def check_weather_effect_MCTS(game_state : "GameState", weather_effect: str) -> str:

        if weather_effect in game_state.active_weather_effect:
            return "already happened"

        game_state.active_weather_effect.add(weather_effect)

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
            game_state.active_weather_effect.clear()

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
            biting_frost(game_state.ai_player_state)
            biting_frost(game_state.opponent_state)

        elif weather_effect == "impenetrable fog":
            impenetrable_fog(game_state.ai_player_state)
            impenetrable_fog(game_state.opponent_state)

        elif weather_effect == "torrential rain":
            torrential_rain(game_state.ai_player_state)
            torrential_rain(game_state.opponent_state)

        elif weather_effect == "skellige storm":
            if "torrential rain" in game_state.active_weather_effect and "impenetrable fog" in game_state.active_weather_effect:
                return "already happened"
            elif "torrential rain" in game_state.active_weather_effect:
                impenetrable_fog(game_state.ai_player_state)
                impenetrable_fog(game_state.opponent_state)
            elif "impenetrable fog" in game_state.active_weather_effect:
                torrential_rain(game_state.ai_player_state)
                torrential_rain(game_state.opponent_state)

        elif weather_effect == "clear weather":
            if game_state.active_weather_effect:
                clear_weather(game_state.ai_player_state)
                clear_weather(game_state.opponent_state)
            else:
                return "already happened"



    @staticmethod
    def maintain_effect_logic(player: Union[Player, PlayerState], card: Card) -> None:

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
