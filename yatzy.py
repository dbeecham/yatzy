from random import randrange
from itertools import combinations

def random_die():
    """ Returns a number between 1 and 6."""
    return randrange(1, 6)


def yatzy_dice():
    """ A yatzy hand; 5 random numbers between 1 and 6. """
    return [random_die() for _ in range(5)]


def reroll_selected_dice(selected_dice, yatzy_dice):
    """ Rerolls indexes selected_dice from yatzy_dice. """
    for die in selected_dice:
        yatzy_dice[die] = random_die()


def get_user_list(question):
    """ Asks the user for a list of space separated numbers.
        Returns a list of numbers. """
    return [int(s) for s in input(question).split()]


def yatzy_card(players):
    """ Generate the yatzy protocol, an n by 15 array of zeroes. """
    return [[0 for x in range(0, 14)] for x in range(players)]


def yatzy_rule(n):
    """ Returns a rule-function given a line on the yatzy
        protocol. The rule function takes a list of dice as
        argument (of length 5), and returns points according
        to that rule. """
    def ones(dice):
        """ Count ones in list. """
        return sum([x for x in dice if x == 1])

    def twos(dice):
        """ Count twos in list. """
        return sum([x for x in dice if x == 2])

    def threes(dice):
        """ Count threes in list. """
        return sum([x for x in dice if x == 3])

    def fours(dice):
        """ Count fours in list. """
        return sum([x for x in dice if x == 4])

    def fives(dice):
        """ Count fives in list. """
        return sum([x for x in dice if x == 5])

    def sixes(dice):
        """ Count sixes in list. """
        return sum([x for x in dice if x == 6])

    def pair(dice):
        """ Return sum of highest pair in list. """

        def max_or_zero(list):
            """ Returns maximum value of a list; 0 if list is empty. """
            try:
                return max(list)
            except ValueError:
                return 0

        return 2 * max_or_zero([i for i, j in combinations(dice, 2) if i == j])
    
    def double_pair(dice):
        """ TODO! """

        # Sentinel value.
        return 1

    def threes(dice):
        """ Find a set of three equal values in list dice
            and return its sum. Returns 0 if nothing found."""
        for i, j, k in combinations(dice, 3):
            if i == j == k:
                return 3 * i

        return 0

    def fours(dice):
        """ Find a set of four equal values in list dice
            and return its sum. Returns 0 if nothing found."""
        for i, j, k, l in combinations(dice, 4):
            if i == j == k == l:
                return 4 * i

        return 0

    def small_straight(dice):
        """ Checks the list dice for the exact combination
            [1, 2, 3, 4, 5] (the small straight) and returns
            its sum. Returns 0 if nothing found."""
        if sorted(dice) == [1, 2, 3, 4, 5]:
            return sum(dice)
        return 0

    def big_straight(dice):
        """ Checks the list dice for the exact combination
            [2, 3, 4, 5, 6] (the large straight) and returns
            its sum. Returns 0 if nothing found."""
        if sorted(dice) == [2, 3, 4, 5, 6]:
            return sum(dice)
        return 0

    def house(dice):
        """ Try to find a house in the list of cards
            i.e. [2, 2, 2, 3, 3] or [5, 5, 4, 4, 4] and
            return its sum. Returns 0 if nothing found."""
        s = sorted(dice)
        if ((s[0] == s[1] == s[2] and s[3] == s[4]) or
           (s[0] == s[1] and s[2] == s[3] == s[4])):
               return sum(dice)
        return 0

    def chance(dice):
        """ Returns the sum of dice. """
        return sum(dice)

    def yatzy(dice):
        """ If every value in list dice is equal, return its sum.
            Else, return 0. """
        if (dice[0] == dice[1] == dice[2] == dice[3] == dice[4]):
            return 50
        return 0

    return [ones, twos, threes, fours, fives, sixes, pair, double_pair,
            threes, fours, small_straight, big_straight, house, chance, yatzy][n]


def yatzy(number_of_players):
    """ Play a game of yatzy! """

    def print_dice(dice):
        """ Pretty-print dice. """
        print()
        print(" (1) (2) (3) (4) (5)")
        print(" ", "   ".join([str(x) for x in dice]))
        print()

    def print_card(card):
        """ Pretty-print a users protocol. """

        titles = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", 
                  "One pair", "Two Pairs", "Three of", "Four of", "Straigth",
                  "Big straight", "House", "Yatzy"]
        
        print("+---------+-----------------+-------+")
        print("|  Index  |      Name       | Score |")
        print("+---------+-----------------+-------+")

        for i in range(len(card)):
            print("| {:>7} | {:<15} | {:<5} |".format(i, titles[i], card[i]))

        print("+---------+-----------------+-------+")
            

    card = yatzy_card(number_of_players)

    # There are 14 turns for each user in a Yatzy game.
    for _ in range(15):
        for player in range(number_of_players):

            print("+-----------------------------------+")
            print("|      Player {:>3}'s turn!           |".format(player + 1))
            print("+-----------------------------------+")

            # Throw dice and print them out.
            dice = yatzy_dice()
            print_dice(dice)

            # Ask the user if he/she would like to reroll. Print result.
            reroll_selected_dice([x - 1 for x in get_user_list("Reroll: ")], dice)
            print_dice(dice)

            # Do it again! You get two rerolls.
            reroll_selected_dice([x - 1 for x in get_user_list("Reroll: ")], dice)
            print_dice(dice)

            # Print the card and let the user select which line
            # he/she would like to use. Use that lines rule-function
            # and store the result in the card (protocol).
            # Finally, we'll print the updated card.
            print_card(card[player])
            rule = int(input("Select line: "))
            card[player][rule] = yatzy_rule(rule)(dice)
            print_card(card[player])
