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
    player_one_deck.load_card_from_db(r"C:\Users\jaisu\PycharmProjects\GwentClone\DB\cards.db")
    player_two_deck = Deck("nilfgaardian")
    player_two_deck.load_card_from_db(r"C:\Users\jaisu\PycharmProjects\GwentClone\DB\cards.db")

    #creating leaders now
    #will ask player what leader they want

    #will eventually change so that it will also be handle in deck

    leader_player_one =  CardLoader.load_leader_card_from_db(r"C:\Users\jaisu\PycharmProjects\GwentClone\DB\leader_cards.db")
    leader_player_two = CardLoader.load_leader_card_from_db(r"C:\Users\jaisu\PycharmProjects\GwentClone\DB\leader_cards.db")


    # Player one leader selection
    # also add a faction check by comparing it to the player's deck
    # basically deck's faction must equal the leader's card faction
    player_one_leader_card = None
    while not player_one_leader_card:
        player_one_leader_choice = input("Player one, what leader do you want for your deck: ").strip().lower()
        for leader_card in leader_player_one:
            if leader_card.leader_name.strip().lower() == player_one_leader_choice and leader_card.faction.lower().strip() == player_one_deck.faction_name.lower().strip():
                player_one_leader_card = leader_card
                break
        #because it will still be None since nothing was assigned to them
        if not player_one_leader_card:
            print(f"Invalid leader name or invalid faction. As a reminder your deck is {player_one_deck.faction_name}. Please try again.")

    # Player two leader selection
    player_two_leader_card = None
    while not player_two_leader_card:
        player_two_leader_choice = input("Player two, what leader do you want for your deck: ").strip().lower()
        for leader_card in leader_player_two:
            if leader_card.leader_name.strip().lower() == player_two_leader_choice and leader_card.faction.lower().strip() == player_two_deck.faction_name.lower().strip():
                player_two_leader_card = leader_card
                break
        #because it will still be None since nothing was assigned to them
        if not player_two_leader_card:
            print(f"Invalid leader name or invalid faction. As a reminder your deck is {player_two_deck.faction_name}. Please try again.")

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

        #I will set each player passed to be false, so that if it changed during one of the previous loops, it gets reset
        game_state.player_one.passed = False
        game_state.player_two.passed = False


        #these are the turns
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

            #we are now going to reset the card choice here to be careful
            first_turn_card_choice = None

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


            #going to ask the user to play their card
            if len(first_turn.hand) != 0:
                first_turn_card_choice = input("\n Please pick a card in your hand to play")

                #now we are going to play card
                played_card_first_turn = first_turn.play_card(first_turn_card_choice)

                #deciding which effect to use
                if played_card_first_turn.card_type == "unit":
                    game_state.use_card_ability(first_turn,played_card_first_turn)
                    #the effects should only have to be maintained by unit cards
                    game_state.maintain_effect(first_turn, played_card_first_turn)
                elif played_card_first_turn.card_type == "weather":
                    game_state.check_weather_effect(played_card_first_turn.ability)
                elif played_card_first_turn.card_type == "buff" and played_card_first_turn.ability == "scorch":
                    game_state.check_buff(first_turn, played_card_first_turn)
                elif played_card_first_turn.card_type == "buff" and played_card_first_turn.ability == "horn":
                    chosen_row = game_state.check_buff(first_turn, played_card_first_turn)
            else:
                print("You have no cards in your deck")





        print(f"{second_turn.player_name}'s turn is now")

        print()
        game_state.display_board()
        print()

        # now initializing the loop for the first player
        while not second_turn.passed or second_turn.hand == 0:

            # we are now going to reset the card choice here to be careful
            second_turn_card_choice = None

            game_state.display_player_hand(second_turn)

            # checking whether the playing wants to pass their turn
            second_turn.passing_turn()

            # this case will leave the loop if the player chooses to leave
            if second_turn.passed:
                print(f"{second_turn.player_name} has passed their turn.")
                break  # or continue, depending on structure

            # now checking whether a user wants to use their leader
            # this is happening in the game class because this ability affects the whole board

            leader_choice = input("Do you want to use your leader card?")

            if leader_choice.lower().strip() == "yes":
                game_state.use_leader_ability(second_turn)

            # going to ask the user to play their card
            if len(second_turn.hand) != 0:
                second_turn_card_choice = input("\n Please pick a card in your hand to play")

                # now we are going to play card
                played_card_second_turn = second_turn.play_card(second_turn_card_choice)

                # deciding which effect to use
                if played_card_second_turn.card_type == "unit":
                    game_state.use_card_ability(second_turn, played_card_second_turn)
                    # the effects should only have to be maintained by unit cards
                    game_state.maintain_effect(second_turn, played_card_second_turn)
                elif played_card_second_turn.card_type == "weather":
                    game_state.check_weather_effect(played_card_second_turn.ability)
                elif played_card_second_turn.card_type == "buff" and played_card_second_turn.ability == "scorch":
                    game_state.check_buff(second_turn, played_card_second_turn)
                elif played_card_second_turn.card_type == "buff" and played_card_second_turn.ability == "horn":
                    chosen_row = game_state.check_buff(second_turn, played_card_second_turn)
            else:
                print("You have no cards in your deck")

        print()
        game_state.display_board()
        print()

        #this block should probably be changed
        #something are wrong with these functions

        #should calculate strength first for both players
        game_state.calculate_strength(first_turn)

        game_state.calculate_strength(second_turn)

        print()

        #now determine the winner
        round_winner = game_state.determine_winner()

        print()

        game_state.faction_ability(round_winner)

        #showing off the game stats
        game_state.round_summary()

        #now we should be resetting the round
        game_state.round_resolve()

        #checking whether the game should end or not and who is the winner
        game_state.end_game_checker()




#over here is the executable
if __name__ == "__main__":
    main()


