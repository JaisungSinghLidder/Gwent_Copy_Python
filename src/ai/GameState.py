from operator import contains

from src.ai.PlayerState import PlayerState
from dataclasses import dataclass, field
from typing import Set, List, Union, Optional

from src.general_game_space.GameLogic import GameLogic
from src.general_game_space.PlayerLogic import PlayerLogic
from src.cards.Card import Card
from copy import deepcopy


import random

#a dataclass that should provide a snapshot view of the general game information
#this will allow the MCTS to evaluate these conditions

@dataclass(frozen = False)
class GameState:
    ai_player_state: PlayerState
    opponent_state: PlayerState
    round_counter: int
    active_weather_effect: Set[str]

    #this class will handle what is playable in the AI player's hand
    #the AI need this class because it needs to be able to discern what it can do so that when it generates the tree
    #isn't filled with wrong moves
    #IMPLEMENTATION_NOTE: this method need to be pretty comprehensive and prevent any illegal moves
    #this will also filter out bad moves that serve no purpose
    def get_legal_moves(self, player: PlayerState) -> List[Union[Card, str]]:

        opponent = None

        if player == self.ai_player_state:
            opponent = self.opponent_state
        else:
            opponent = self.ai_player_state

        legal_moves = []

        #this case is for the leader
        #we are going to append a string because using a leader card is a special case
        # now we need to check for faction and illegal moves for that faction in tow
        if not player.leader_used:

            #okay now we need to check for behaviour of players
            #might need to create a sub function

            #northen realms is going to be a simple weather check
            if player.faction == "northern realms":
                if self.active_weather_effect:
                    legal_moves.append("USE_LEADER")

            elif player.faction == "nilfgaardian":
                if opponent.hand:
                    legal_moves.append("USE_LEADER")

            #doubling the spy card by two
            elif player.faction == "monsters":
                #check whether there is a spy to double on the board
                thereSpy = False

                for row in ["melee", "range", "siege"]:
                    for card in player.board[row]:
                        if card.ability == "spy":
                            thereSpy = True

                    if thereSpy:
                        legal_moves.append("USE_LEADER")

            elif player.faction == "scoia'tael":
                # because it's always going to be with a deck
                # we can just append this rule

                legal_moves.append("USE_LEADER")

            elif player.faction == "skillege":

                if player.graveyard:
                    legal_moves.append("USE_LEADER")




        # running through the cards through the hand
        for card in player.hand:

            #checking here if the medic card can target any graveyard card
            if card.ability == "medic":
                if not player.graveyard:
                    continue
            #checking the cards here
            legal_moves.append(card)

            #we need to append the commander horn ability
            #what to do here, this here needs to change
            #the logic is weak!
            if card.ability == "horn":
                #checking whether there are any cards in the player's board
                has_any_cards = any(player.board[row] for row in ["melee", "range", "siege"])

                #skip this card if there is no card on the board period
                if not has_any_cards:
                    continue

                if any(player.board["melee"]):
                    horn_row = "melee"
                    legal_moves.append((card,horn_row))

                if any(player.board["range"]):
                    horn_row = "range"
                    legal_moves.append((card, horn_row))

                if any(player.board["siege"]):
                    horn_row = "siege"
                    legal_moves.append((card, horn_row))




            #going to make it illegal for the ai that if the no cards, it shouldn't play scorch
            #also if there is only hero cards, as hero cards are unaffected by scorch
            if card.ability == "scorch":
                # Assume that all cards are heroes until proven otherwise
                only_heroes = True

                #checking if there is any cards in the opponent state
                has_any_cards = any(opponent.board[row] for row in ["melee", "range", "siege"])

                #if the opponent has no cards, then why bother with scorching it?
                if not has_any_cards:
                    continue


                for row in ["melee", "range","siege"]:
                    for opponent_card in opponent.board[row]:
                        if opponent_card.ability != "hero":
                            only_heroes = False
                            break

                    if not only_heroes:
                        break



                if not only_heroes:
                    legal_moves.append(card)


            if card.card_type == "weather":

                if card.card_name not in self.active_weather_effect:
                    legal_moves.append(card)




        #allowing the passing the turn
        legal_moves.append("PASS")


        return legal_moves


    #lots of integration with the apply moves
    #so this will take only one legal move so that it can build the tree piece by piece through it children

    #might need to change this to be more flexible
    def apply_move(self, move: Union[Card, str], row: Optional[str], player: PlayerState) -> "GameState":

        new_state = deepcopy(self)

        if isinstance(move, str):
            if move == "PASS":

                if player == self.ai_player_state:
                    new_state.ai_player_state.passed = True
                else:
                    new_state.opponent_state.passed = True

            #need to play leader
            elif move == "USE_LEADER":
                if player == self.ai_player_state:
                    new_state.ai_player_state.passed = True
                else:
                    new_state.opponent_state.passed = True

        if isinstance(move, Card):
            #need to use the player logic
            #the basic unit
            if move.ability == "unit":


                if player == self.ai_player_state:

                    PlayerLogic.play_card(new_state.ai_player_state, move.card_name)

                    GameLogic.maintain_effect_logic(new_state.ai_player_state, move)

                else:
                    PlayerLogic.play_card(new_state.opponent_state, move.card_name)

                    GameLogic.maintain_effect_logic(new_state.opponent_state, move)



            elif move.ability == "weather":

                GameLogic.check_weather_effect_MCTS(new_state, move.card_name)

            elif move.ability == "buff":

                #checking whether it is a scorch or a horn case

                #horn

                if player == self.ai_player_state:

                    if row:
                        GameLogic.check_buff_logic(new_state, new_state.ai_player_state, move, row)
                    # scorch
                    else:
                        GameLogic.check_buff_logic(new_state, new_state.ai_player_state, move)

                else:

                    if row:
                        GameLogic.check_buff_logic(new_state, new_state.opponent_state, move, row)
                    # scorch
                    else:
                        GameLogic.check_buff_logic(new_state, new_state.opponent_state, move)


        return new_state

    #this will use the end game checker to checker whether the game is ended, should be pretty similar
    #just caring whether the game has ended or not.

    def is_terminal(self) -> bool:
        result = GameLogic.end_game_checker(self)

        #simply check to see which result it finalize

        if result == "draw" or result == "player one wins" or result == "player two wins":
            return True
        else:
            return False


    #complicated structure here that will have to reward certain actions for the ai to deem better actions versus worse actions
    #the get reward will read itself.
    def get_reward(self, is_terminal_result: bool) -> float:

        #just setting the reward here just in case
        reward = 0


        #this reward structure has two cases

        #the first case is simply checking if it can win, if it terminal, it will take the win, or the draw, and if worst-case, it will take the worst

        #checking whether it is a terminal victory:
        if is_terminal_result:
            result = GameLogic.end_game_checker(self)


            #ai is player two
            if result == "player two wins":
                reward += 8.0
            elif result == "player one wins":
                reward -= 8.0
            else:
                #just showcasing that a draw will neither harm nor show gain to a player
                reward += 0

        #now showing the
        else:
            #getting how many cards' are in the ai's hand
            ai_hand = len(self.ai_player_state.hand)

            #giving a reward on how many cards it has it own hand
            reward += 0.1 * ai_hand

            #dealing with if the power is better or not
            if self.ai_player_state.sum > self.opponent_state.sum:
                reward += 0.8
            else:
                reward -= 0.8

            #dealing with players' lives
            if self.ai_player_state.lives > self.opponent_state.lives:
                reward += 0.6
            else:
                reward -= 0.6

            #case where it all horns are affected
            if self.ai_player_state.siege_row_horn_effect and self.ai_player_state.range_row_horn_effect and self.ai_player_state.melee_row_horn_effect:
                #creating a counter for cards
                cardCounter = 0

                for row in ["melee", "range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

            #case where it siege and range
            elif self.ai_player_state.siege_row_horn_effect and self.ai_player_state.range_row_horn_effect:
                #creating a counter for cards
                cardCounter = 0

                for row in ["range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter


            #case where it is siege and melee
            elif self.ai_player_state.siege_row_horn_effect and self.ai_player_state.melee_row_horn_effect:
                #creating a counter for cards
                cardCounter = 0

                #rewarding it for cards in these row
                for row in ["melee", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

            #case with range and melee
            elif self.ai_player_state.siege_row_horn_effect and self.ai_player_state.range_row_horn_effect and self.ai_player_state.melee_row_horn_effect:
                #creating a counter for cards
                cardCounter = 0

                for row in ["melee", "range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

            #case with siege
            elif self.ai_player_state.siege_row_horn_effect:
                #creating a counter for cards
                cardCounter = 0

                for row in ["siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee", "range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

            # case with range
            elif self.ai_player_state.range_row_horn_effect:
                # creating a counter for cards
                cardCounter = 0

                for row in ["range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

            # case with melee
            elif self.ai_player_state.range_row_horn_effect:
                # creating a counter for cards
                cardCounter = 0

                for row in ["melee"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

                cardCounter = 0

                for row in ["range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter



            # case where it all weather are affected
            if self.ai_player_state.range_row_weather_effect and self.ai_player_state.range_row_weather_effect  and self.ai_player_state.melee_row_weather_effect:
                # creating a counter for cards
                cardCounter = 0

                for row in ["melee", "range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

            # case where it siege and range
            elif self.ai_player_state.siege_row_weather_effect  and self.ai_player_state.range_row_weather_effect :
                # creating a counter for cards
                cardCounter = 0

                for row in ["range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter


            # case where it is siege and melee
            elif self.ai_player_state.siege_row_weather_effect  and self.ai_player_state.melee_row_weather_effect :
                # creating a counter for cards
                cardCounter = 0

                # rewarding it for cards in these row
                for row in ["melee", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

            # case with range and melee
            elif self.ai_player_state.siege_row_weather_effect  and self.ai_player_state.range_row_weather_effect  and self.ai_player_state.melee_row_weather_effect :
                # creating a counter for cards
                cardCounter = 0

                for row in ["melee", "range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

            # case with siege
            elif self.ai_player_state.siege_row_horn_effect:
                # creating a counter for cards
                cardCounter = 0

                for row in ["siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee", "range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

            # case with range
            elif self.ai_player_state.range_row_weather_effect :
                # creating a counter for cards
                cardCounter = 0

                for row in ["range"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["melee", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

            # case with melee
            elif self.ai_player_state.range_row_weather_effect :
                # creating a counter for cards
                cardCounter = 0

                for row in ["melee"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward -= 0.2 * cardCounter

                cardCounter = 0

                for row in ["range", "siege"]:
                    for card in self.ai_player_state.board[row]:
                        cardCounter += 1

                reward += 0.2 * cardCounter

    #creating a hash function
    def __hash__(self):
        return hash((
            self.ai_player_state,
            self.opponent_state,
            self.round_counter,
            frozenset(self.active_weather_effect)
        ))


    #creating a get random function so that during rollout it can play moves that the MCTS can compare against
    #because we need to further the game on human side during the simulation
    #just choosing random moves for simplicity
    #could later make a rule based one or even a min MCTS for the main MCTS to play against

    def get_random_move(self, legal_moves: List[Union[Card, str]] ) -> Union[Card, str]:

        random_move = random.choice(legal_moves)

        return random_move






















