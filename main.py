from Card_Space.Deck import Deck
from General_Game_Space.Player import Player
from Card_Space.CardLoader import CardLoader

#this main function will run the game and it's loop
def main():

    #intializing the decks for the player
    #their faction is already intialized when the deck is created
    player_one_deck = Deck("northern realms")
    player_one_deck.load_deck_from_json("Card_Space/cards.json")
    player_two_deck = Deck("nilfgaardian")
    player_two_deck.load_deck_from_json("Card_Space/cards.json" )

    #creating leaders now
    #will ask player what leader they want

    leader_player_one =  CardLoader.load_leaders_from_json("Card_Space/leader_cards.json")
    leader_player_two = CardLoader.load_leaders_from_json("Card_Space/leader_cards.json")

    player_one_leader_choice = input("Player one, what leader do you want for your deck")

    player_one_leader_card = None
    player_two_leader_card = None

    for card in leader_player_one:
        if card == player_one_leader_choice:
            player_one_leader_card = card

    for card in leader_player_two:
        if card == player_two_leader_card:
            player_two_leader_card = card

    #creating the players now

    player_one = Player(player_one_deck, player_one_leader_card, "northern realms", False, "Dave")
    player_two = Player(player_two_deck, player_two_leader_card, "nilfgaardian", False, "Steve")






#over here is the executable
if __name__ == "__main__":
    main()




