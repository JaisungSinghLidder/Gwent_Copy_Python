import copy

from src.general_game_space.Game import Game
from src.general_game_space.Player import Player
from src.ai.GameState import GameState
from src.ai.PlayerState import PlayerState


#this class is going to extract the information from the game class to the GameState class

class GameStateExtractor():

    @staticmethod
    def extract_game(game : Game) -> GameState:

        #creating both player
        #afterward I will create a sub function that will reduce this code

        def extract_player_info(player: Player):
            playerHand = copy.deepcopy(player.hand)
            playerGraveyard = copy.deepcopy(player.graveyard)
            playerLives = copy.deepcopy(player.lives)
            playerBoard = copy.deepcopy(player.board)
            playerPassed = copy.deepcopy(player.passed)
            playerSum = copy.deepcopy(player.sum)
            playerLeaderUsed = copy.deepcopy(player.leader_used)
            playerLeaderCard = copy.deepcopy(player.leader_card)
            playerFaction = copy.deepcopy(player.faction)
            playerAIPlayer = copy.deepcopy(player.ai_player)
            player_name = copy.deepcopy(player.player_name)
            melee_row_weather_effect = copy.deepcopy(player.melee_row_weather_effect)
            range_row_weather_effect = copy.deepcopy(player.range_row_weather_effect)
            siege_row_weather_effect = copy.deepcopy(player.siege_row_weather_effect)
            melee_row_horn_effect = copy.deepcopy(player.melee_row_horn_effect)
            range_row_horn_effect = copy.deepcopy(player.range_row_horn_effect)
            siege_row_horn_effect = copy.deepcopy(player.siege_row_horn_effect)

            #formatted for easier view of variables for me
            return PlayerState(
                playerHand,
                playerGraveyard,
                playerLives,
                playerBoard,
                playerPassed,
                playerSum,
                playerLeaderUsed,
                playerLeaderCard,
                playerFaction,
                playerAIPlayer,
                player_name,
                melee_row_weather_effect,
                range_row_weather_effect,
                siege_row_weather_effect,
                melee_row_horn_effect,
                range_row_horn_effect,
                siege_row_horn_effect
            )

        playerOneState = extract_player_info(game.player_one)

        playerTwoState = extract_player_info(game.player_two)

        #now creating part of the game structure
        gameStateRoundCounter = copy.deepcopy(game.round_counter)

        gameWeatherRow = copy.deepcopy(game.active_weather_effect)

        #here we are going to check whether the player is AI

        if (playerOneState.ai_player):
            gameSnapShot = GameState(playerOneState, playerTwoState, gameStateRoundCounter, gameWeatherRow)
        else:
            gameSnapShot = GameState(playerTwoState, playerOneState, gameStateRoundCounter, gameWeatherRow)


        return gameSnapShot

