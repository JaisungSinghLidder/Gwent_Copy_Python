from src.ai.GameState import GameState
from src.ai.PlayerState import PlayerState
from src.general_game_space import Game, Player
from typing import Union

#creating this class so that we can have pure functions here that don't rely on printing information so that both the AI class and this regular game class can use it

#okay, for today we are just simplifying the logic

class GameLogic:

    @staticmethod
    def determine_round_winner(game_or_gamestate: Union[Game, GameState]) -> str:

        def determining_winner_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player,PlayerState]):
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
        elif isinstance(game_or_gamestate, GameState):
            determining_winner_player_input(game_or_gamestate.ai_player_state, game_or_gamestate.opponent_state)
        else:
            raise ValueError("Must input either a Game or GameState class")



    #note that we need the card and the player card

    @staticmethod
    def use_card_ability(game_or_game_state: Union[Game, GameState], player: Union[Player,  PlayerState], og_card) -> None:


        def use_card_ability_player_input(player_one: Union[Player, PlayerState], player_two: Union[Player,PlayerState]):

            opponent = None

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

            elif og_card.ability.lower().strip() == "medic":
                if not player.graveyard:
                    print("There is no cards to heal")
                else:
                    for card in player.graveyard:
                        print(card.card_name)
                    card_choice = input("So what card do you want?")
                    for i, c in enumerate(player.graveyard):
                        if c.card_name == card_choice and c.card_type == "unit" and c.ability != "hero":
                            row = c.row
                            player.board[row].append(c)
                            del player.graveyard[i]
                            break

            elif og_card.ability.lower().strip() == "muster":
                for i, card in enumerate(player.deck):
                        if og_card == card:
                            player.board[card.row].append(card)
                            # we are using del so that we delete the specific index and not deleting all the cards with the same name
                            del player.deck[i]

            elif og_card.ability.lower().strip() == "morale boost":
                for card in player.board[og_card.row]:
                    if og_card.card_name != card.card_name:
                        card.current_strength += 1

            elif og_card.ability.lower().strip() == "spy":
                #spy's go on opponent's board
                opponent.board[og_card.row].append(og_card)
                for _ in range(2):
                    card = player.deck.draw_from_deck()
                    if card:
                        player.hand.append(card)

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
            elif isinstance(game_or_game_state, GameState):
                use_card_ability_player_input(game_or_game_state.ai_player_state, game_or_game_state.opponent_state)
            else: 
                raise ValueError("Must input either a Game or GameState class")

        @staticmethod
        def end_game_checker(game_or_game_state: Union[Game, GameState]) -> str:

            if isinstance(game_or_game_state, Game):
                p1_nilfgaardian = game_or_game_state.player_one.faction.lower() == "nilfgaardian"
                p2_nilfgaardian = game_or_game_state.player_two.faction.lower() == "nilfgaardian"

                # using <= just to make sure if a glitch happens and something became negative that it would error check for that.
                if game_or_game_state.player_one.lives <= 0 and game_or_game_state.player_two.lives <= 0:
                    if not p1_nilfgaardian and not p2_nilfgaardian:
                        return "draw"
                    elif p1_nilfgaardian and not p2_nilfgaardian:
                        return "player one wins"
                    elif not p1_nilfgaardian and p2_nilfgaardian:
                        return "player two wins"
                elif game_or_game_state.player_one.lives <= 0:
                    return "player two wins"
                elif game_or_game_state.player_two.lives <= 0:
                    return "player one wins"

            elif isinstance(game_or_game_state, GameState):
                p1_nilfgaardian = game_or_game_state.ai_player_state.faction.lower() == "nilfgaardian"
                p2_nilfgaardian = game_or_game_state.opponent_state.faction.lower() == "nilfgaardian"

                # using <= just to make sure if a glitch happens and something became negative that it would error check for that.
                if game_or_game_state.ai_player_state.lives <= 0 and game_or_game_state.opponent_state.lives <= 0:
                    if not p1_nilfgaardian and not p2_nilfgaardian:
                        return "draw"
                    elif p1_nilfgaardian and not p2_nilfgaardian:
                        return "player one wins"
                    elif not p1_nilfgaardian and p2_nilfgaardian:
                        return "player two wins"
                elif game_or_game_state.ai_player_state.lives <= 0:
                    return "player two wins"
                elif game_or_game_state.opponent_state.lives <= 0:
                    return "player one wins"



