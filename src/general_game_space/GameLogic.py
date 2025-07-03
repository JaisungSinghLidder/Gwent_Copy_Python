from src.ai.GameState import GameState
from src.general_game_space import Game
from typing import Union

#creating this class so that we can have pure functions here that don't rely on printing information so that both the AI class and this regular game class can use it

class GameLogic:

    @staticmethod
    def determine_round_winner(game_or_gamestate: Union[Game, GameState]) -> str:

        #now handling whether it is a gameState or game class
        if isinstance(game_or_gamestate, Game):
            if game_or_gamestate.player_one.sum > game_or_gamestate.player_two.sum:
                game_or_gamestate.player_two.lose_life()
                print(f"{game_or_gamestate.player_one.player_name} has won the round")
                return "player one wins"
            elif game_or_gamestate.player_two.sum > game_or_gamestate.player_one.sum:
                game_or_gamestate.player_one.lose_life()
                print(f"{game_or_gamestate.player_two.player_name}has one the round")
                return "player two wins"
            # Tie cases
            elif game_or_gamestate.player_one.sum == game_or_gamestate.player_two.sum:
                game_or_gamestate.player_one.lose_life()
                game_or_gamestate.player_two.lose_life()
                return "draw"
        elif isinstance(game_or_gamestate, Game):
            #need to add the lost_life() to the game state
            if game_or_gamestate.ai_player_state.sum > game_or_gamestate.opponent_state.sum:
                game_or_gamestate.opponent_state.lose_life()
            elif game_or_gamestate.opponent_state.sum > game_or_gamestate.ai_player_state.sum:
                game_or_gamestate.opponent_state.lose_life()
            elif game_or_gamestate.ai_player_state == game_or_gamestate.opponent_state.sum:
                game_or_gamestate.ai_player_state.lose_life()
                game_or_gamestate.opponent_state.lose_life()
        else:
            raise ValueError("Input must be Game or GameState")