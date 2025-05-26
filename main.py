from Card_Space.Card import Card
from Card_Space.Deck import Deck
from Faction_Space.Leader import Leader
from General_Game_Space.Game import Game
from General_Game_Space.Player import Player

#this main function will run the game and it's loop
def main():

    #intializing the decks for the player
    player_one_deck = Deck("northern realms")
    player_one_deck.load_deck_from_json("Card_Space/cards.json", "northern realm")
    player_two_deck = Deck("nilfgaardian")
    player_two_deck.load_deck_from_json("Card_Space/cards.json", "nilfgaardian", )

    #creating the players now

    player_one = Player(player_one_deck, )





#over here is the executable
if __name__ == "__main__":
    main()


