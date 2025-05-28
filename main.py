from Card_Space.Deck import Deck
from General_Game_Space.Player import Player
from Card_Space.CardLoader import CardLoader
from General_Game_Space.Game import Game

#this main function will run the game and it's loop
def main():

    #this is going to hold the played card
    played_card_first_turn = None
    played_card_second_turn = None
    #going to hold the chosen_row in the commander's horn case
    chosen_row_first_turn = None
    chosen_row_second_turn = None
    #intializing the decks for the player
    #their faction is already intialized when the deck is created
    player_one_deck = Deck("northern realms")
    player_one_deck.load_deck_from_json(r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\cards.json")
    player_two_deck = Deck("nilfgaardian")
    player_two_deck.load_deck_from_json(r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\cards.json")

    #creating leaders now
    #will ask player what leader they want

    leader_player_one =  CardLoader.load_leaders_from_json(r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\leader_cards.json")
    leader_player_two = CardLoader.load_leaders_from_json(r"C:\Users\jaisu\PycharmProjects\GwentClone\Card_Space\leader_cards.json")

    player_one_leader_choice = input("Player one, what leader do you want for your deck ")

    player_one_leader_card = None
    player_two_leader_card = None

    for card in leader_player_one:
        if card == player_one_leader_choice:
            player_one_leader_card = card

    player_two_leader_card = input("Player two, what leader do you want for your deck ")

    for card in leader_player_two:
        if card == player_two_leader_card:
            player_two_leader_card = card

    #creating the players now

    player_one = Player(player_one_deck, player_one_leader_card, "northern realms", False, "Dave")
    player_two = Player(player_two_deck, player_two_leader_card, "nilfgaardian", False, "Steve")

    #now creating the game state

    game_state = Game(player_one, player_two)

    #now we will decide who goes first
    game_state.determine_turn_order()

    #players should now draw their deck
    game_state.player_starting_draw()


    #because there is 3 rounds, I am simply going to run a for loop that goes around 3 times
    for _ in range(3):
        first_turn = None
        second_turn = None

        #need to add a block to decide which player goes first
        if game_state.player_one.turn_order_first:
            first_turn = game_state.player_one
            second_turn = game_state.player_two

            print(f"{game_state.player_one.player_name} is going first")
        else:
            first_turn = game_state.player_one
            second_turn = game_state.player_two
            print(f"{game_state.player_two.player_name} is going first")

        #playing now any cards that have been kept, the faction ability will save any cards and play it here
        #however, no point to use this if it's the first round since no ability works in that way
        if game_state.round_counter != 1:
            game_state.play_card_to_keep()

        #now initializing the loop for the first player
        while not first_turn.passed or first_turn.hand == 0:

            game_state.display_player_hand(first_turn)

            #checking whether the playing wants to pass their turn
            first_turn.passing_turn()

            #this case will leave the loop if the player chooses to leave
            if first_turn.passed:
                print(f"{first_turn.player_name} has passed their turn.")
                break  # or continue, depending on structure

            #now checking whether a user wants to use their leader
            #this is happening in the game class because this ability affects the whole board

            leader_choice = input("Do you want to use your leader card?")

            if leader_choice.lower().strip() == "yes":
                game_state.use_leader_ability(first_turn)

            #now we are going to play card
            played_card_first_turn = first_turn.play_card()

            #deciding which effect to use
            if played_card_first_turn.card_type == "unit":
                game_state.use_card_ability(first_turn,played_card_first_turn)
            elif played_card_first_turn.card_type == "weather":
                game_state.active_weather_effect(first_turn,played_card_first_turn)
            elif played_card_first_turn.card_type == "buff" and played_card_first_turn.ability == "scorch":
                game_state.check_buff(first_turn, played_card_first_turn)
            elif played_card_first_turn.card_type == "buff" and played_card_first_turn.ability == "horn":
                chosen_row = game_state.check_buff(first_turn, played_card_first_turn)



        print(f"{second_turn.player_name}'s turn is now")


        game_state.display_board()

        # now initializing the loop for the first player
        while not second_turn.passed or second_turn.hand == 0:
            # checking whether the playing wants to pass their turn
            second_turn.passing_turn()

            #checking whether the player should leave
            if second_turn.passed:
                print(f"{second_turn.player_name} has passed their turn.")
                break  # or continue, depending on structure

            # now checking whether a user wants to use their leader
            # this is happening in the game class because this ability affects the whole board

            leader_choice = input("Do you want to use your leader card?")

            if leader_choice.lower().strip() == "yes":
                game_state.use_leader_ability(second_turn)

            # now we are going to play card
            played_card_second_turn = second_turn.play_card()

            # deciding which effect to use
            if played_card_second_turn.card_type == "unit":
                game_state.use_card_ability(first_turn, played_card_second_turn)
            elif played_card_second_turn.card_type == "weather":
                game_state.active_weather_effect(first_turn, played_card_second_turn)
            elif played_card_second_turn.card_type == "buff" and played_card_second_turn.ability == "scorch":
                game_state.check_buff(first_turn, played_card_second_turn)
            elif played_card_second_turn.card_type == "buff" and played_card_second_turn.ability == "horn":
                chosen_row = game_state.check_buff(first_turn, played_card_second_turn)

        #now determine the winner
        game_state.determine_winner()

        #showing off the game stats
        game_state.round_summary()

        #now we should be resetting the round
        game_state.round_resolve()




#over here is the executable
if __name__ == "__main__":
    main()




