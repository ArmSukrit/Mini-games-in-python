import time

from tools import *

# import all games as global functions
from games.fourInARow import four_in_a_row
from games.hangman import hangman
from games.rock_paper_scissors import rock_paper_scissors
from games.confusing_story import confusing_stories
from games.roll_dice import roll_dice
from games.guess_number import guess_number


def problems_or_nice_features():
    """
    - getpass() does not seem to work
    - in multiplayer games, winner announcement should be good looking, ex: use big emoji with winner's name/icon
    - must have a lot of built-in words for hangman (get from RandomWords and save it in a list)
    - 
    """


# do not forget to manually add new game's info into this function
def game_info() -> dict:
    return {
        '1': ('Guess the Number', guess_number),
        '2': ('Roll a dice', roll_dice),
        '3': ('Confusing Stories', confusing_stories),
        '4': ('Rock Paper Scissors', rock_paper_scissors),
        '5': ('Hangman (requires internet connection)', hangman),
        '6': ('4 In A Row (requires 2 players)', four_in_a_row),
    }


# main structure -------------------------------------------------------------------------------------------------------

def main():
    # all_games = {key: (game title, game function)}
    all_games = game_info()

    while True:
        print_intro(all_games)
        decision = get_what_game_to_play(all_games)
        if decision == 'x':
            break

        # call the selected game function
        while True:
            clear_console()
            game_function = all_games[decision][1]
            game_function()

            # replay?
            exception = [roll_dice, rock_paper_scissors]
            if game_function in exception:
                break
            final_decision = input("Enter ---> replay.\n"
                                   "Enter 'x' ---> return to game selection.\n"
                                   "(Enter, x)?: ").strip().lower()
            if final_decision != '':
                break

        clear_console()

    # quit entire program
    print("\nThank you for playing!\nSee you next time. xd")
    time.sleep(5)


# Not game functions ---------------------------------------------------------------------------------------------------


def get_what_game_to_play(all_games: dict) -> str:
    # get and check decision
    decision = ''
    while decision not in all_games.keys():
        decision = input("Enter a game number: ").strip()
        if decision == 'x':
            return decision
        if decision not in all_games.keys():
            print("-----> Invalid game number\n")
    return decision


def print_intro(all_games: dict):
    print("\nAll available games:")
    for num, (title, function) in sorted(all_games.items()):
        print(f'{num}: {title}')
    print('Enter "x" to exit.\n')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
