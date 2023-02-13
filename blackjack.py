
#Creating a class for bank account

import random

class Account:
    
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount
        
    def withdraw(self, num):
        if self.amount - num >=0:
            self.amount = self.amount - num
        else:
            print('Insufficient funds')
        
    def deposit(self, num):
        self.amount += num
        
    def __str__(self):
        return 'There is £' + str(self.amount) + ' in ' + self.name + "'s account."


#creating tuples for the suits, ranks and dictionary values of cards

suits = ('Diamonds', 'Clubs', 'Hearts', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':10}


#Creating a class for individual cards

class Playing_Card():
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
        
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
    def __repr__(self):
        return self.rank + ' of ' + self.suit


#Creating a class for a deck of cards

class Deck:
    
    def __init__(self):
        self.full_deck = []
        for suit in suits:
            for rank in ranks:
                self.full_deck.append(Playing_Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.full_deck)
        
    
    def deal_one(self):
        return self.full_deck.pop()


#Creating a class for each player's hand

class PlayerHand():
    def __init__(self, name):
        self.current_hand = []
        self.name = name
    
    def add_card(self, new_card):
        self.current_hand.append(new_card)
        
    def __str__(self):
        return f'({self.name} has {len(self.current_hand)} cards.'



#CODING OF GAME#

#On new game: #
#First need to set up account with 100 currency #

player_name = input('What is your name?: ')
player_account = Account(player_name, 100)

#Line of code to keep game playing unless changed #

keep_playing = True


while keep_playing:
    print(player_account)

    #Then need to ask total amount to bet #
    
    if player_account.amount <= 0:
        print('Not enough funds - game over')
        break

    def bet_amount():
        bet_value = int(input('How much would you like to bet?: '))

        while bet_value > player_account.amount:
            print('Insufficient funds for this bet, please enter a new value')
            bet_value = int(input('How much would you like to bet?: '))

        return bet_value


    current_bet = bet_amount()

    player_account.withdraw(current_bet)



    #Then need to initialise new deck #

    game_deck = Deck()
    game_deck.shuffle()


    #To actually play game#

    #Create 2 player hands, one for player and other for computer #

    player_hand = PlayerHand(player_name)
    computer_hand = PlayerHand('Computer')


    #Deal two cards to player and computer - dealt in order! #

    player_hand.add_card(game_deck.deal_one())
    computer_hand.add_card(game_deck.deal_one())
    player_hand.add_card(game_deck.deal_one())
    computer_hand.add_card(game_deck.deal_one())



    #Show player 2 cards but only show computer's first card #

    print(f'\nYour current cards: {player_hand.current_hand[0]}, {player_hand.current_hand[1]}')

    print(f"Computer's first card: {computer_hand.current_hand[0]}")



    #Show running total of cards #

    card_total = 0

    for card in player_hand.current_hand:
          card_total += card.value

    print(f'\nYour current card total: {card_total}')



    #If running total <21, add new card or hold #
    #Show running total of cards - if bust then computer automatically wins #
    #Otherwise computer plays #
    #Extra bit for Ace to = 1 if total exceeds 21 #

    def hit_or_hold(x):

        current_card_total = x

        while current_card_total < 21:
            player_choice = input('\nHit or Hold? - Type "1" for hit or "2" for hold: ')
            if player_choice == '1':
                player_hand.add_card(game_deck.deal_one())
                current_card_total += player_hand.current_hand[-1].value
                print(f'Your current cards: ')
                for card in player_hand.current_hand:
                    print(card)
                if current_card_total >21:
                    for card in player_hand.current_hand:
                        if card.rank == 'Ace':
                            card.value = 1
                            current_card_total = 0
                            for card in player_hand.current_hand:
                                current_card_total += card.value
                            break
                print(f'\nCurrent card total: {current_card_total}\n')
            else:
                break
        
        
        return current_card_total

    final_card_total = hit_or_hold(card_total)

    if final_card_total >21:
          print(f"You've gone bust with a total of {final_card_total}")
    elif final_card_total == 21:
          print('Blackjack! Your total is 21')
    else:
          print(f'\nYou finished your turn with a total of {final_card_total}')



    #Computer hits until total >player total or >21 #

    computer_total = 0

    for card in computer_hand.current_hand:
        computer_total += card.value

    print("\nComputer's current cards: ")
    for card in computer_hand.current_hand:
        print(card)

    print(f'\nCurrent computer total: {computer_total}')

    while computer_total <22 and computer_total < final_card_total and final_card_total <= 21:
        computer_hand.add_card(game_deck.deal_one())
        computer_total += computer_hand.current_hand[-1].value
        print("\nComputer's current cards: ")
        for card in computer_hand.current_hand:
            print(card)
        if computer_total >21:
            for card in computer_hand.current_hand:
                if card.rank == 'Ace':
                    card.value = 1
                    computer_total = 0
                    for card in computer_hand.current_hand:
                        computer_total += card.value
                    break
        print(f'\nCurrent computer total: {computer_total}')

    print(f'\nFinal computer total: {computer_total}\n')


    #If player wins, double bet and add to account #
    #If player and computer draw, add only initial bet back to account #
    #If computer wins or player busts, money is lost #

    if final_card_total <= 21 and card_total > computer_total:
        player_account.deposit(2*current_bet)
        print('You win!')
    elif final_card_total <=21 and computer_total > 21:
        player_account.deposit(2*current_bet)
        print('You win!')
    elif final_card_total <=21 and final_card_total == computer_total:
        player_account.deposit(current_bet)
        print("It's a draw")
    else:
        print('You lose!')

    #Asks if player wants to play again #

    print(player_account)
    
    play_again = input('Play again? Type "Y" for Yes or "N" for No: ').upper()
    
    if play_again == 'Y':
        keep_playing = True
    else:
        keep_playing = False