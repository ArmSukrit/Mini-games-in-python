import random
import time
import os


def known_problems():
    """
    1 printing completed story in confusing stories game
    """


# do not forget to manually add new game's info into this function which acts as database
def game_info() -> dict:
    return {
        '1': ('Guess the Number', guess_number),
        '2': ('Roll a dice', roll_dice),
        '3': ('Confusing Stories', confusing_stories),
            }


# Every game function --------------------------------------------------------------------------------------------------

def confusing_stories():
    print("Welcome to Confusing Stories!")

    # stories = {
    #            key: (
    #                  title,
    #                  number of required words,
    #                  required word types,
    #                  story
    #                  )
    #            }
    # Each '@' is meant to be replaced with a word that is a user input
    stories = {
        '1': (
            'Spring Cartoon!',
            10,
            'noun/s, adj, noun, noun/s, noun/s, noun, type of food, noun/s, noun, adjective',
            'Planting a vegetable garden is not only fun, it also helps save @. You will need a piece of @ '
            'land. You may need a @ to keep the @ and @ out. As soon as @ is here you can go out there with '
            'your @ and plant all kinds of @. Then in a few months, you will have corn on the @ and big, @ '
            'flowers.'
            ),
        '2': (
            'Trip to the Park!',
            14,
            'person, adj, adj, noun, adj, noun, adj, adj, verb, verb, person, verb, adj, verb',
            'Yesterday, @ and I went to the park. On our way to the @ park, we saw a @ @ on out bike. '
            'We also saw big @ balloons tied to a @. Once we got to the @ park, the sky turned @. '
            'It started to @ and @. @ and I @ all the way home. Tomorrow we will try to go to the @ '
            'park again and hope it does not @.'
              ),
        '3': (
            'Easter Hunt!',
            11,
            'adj, person, animal, plural noun, plural noun, noun, verb, noun, animal, adj, adj',
            "Today we get to hunt for @ eggs in @'s yard. The Easter @ hid them for us to find! "
            "I am hoping that there will be a basket full of @ and @. Since it's spring, there's lots of "
            "@ on the ground. When I @ through it, I hope it doesn't get on my @. I love that "
            "the Easter @ hides things for us. It makes the @ day so very @!!"
            ),
        '4': (
            'Chocolate Bunny!',
            12,
            "nouns, integer, adj, noun, a game, adj, color, liquid, noun, nouns, noun, adj",
            "Schools are closed at Easter time and all the @ get @ weeks off. The @ teachers also"
            " get a vacation. There are a lot of things to ddo on Easter vacation. Some kids hang "
            "around and watch the @. Others go outside and play @. Little kids will color @ eggs. "
            "They use a package of @ dye. They pour it in a bowl full of @. Then they dip the @ in "
            "the bowl and then rinse it off. After the @ are dried, you place them in the Easter @ "
            "along with a @ chocolate bunny!"
            )
    }

    # inform about stories
    print('\nAll available stories:')
    for key, value in sorted(stories.items()):
        print(f'{key}: {value[0]}  {value[1]} words are required.')

    # get and check input
    decision = ''
    while decision not in stories.keys():
        decision = input('\nEnter a story number: ').strip()
        if decision not in stories.keys():
            print('-----> Invalid story number.')

    # main game sequence
    clear_console()
    title, num, types, story = stories[decision]
    required_words = types.split(', ')
    user_input = []

    print(f'\n{title}')

    invalid_value = ['./,;"(|}{[]<>):', "'-=_+%$#@!^&*"]
    for i, each in enumerate(required_words, 1):
        # input filter
        chosen_word = ''
        invalid = True
        while invalid:
            identified_invalid = set()
            chosen_word = input(f'{i}/{num} Enter {each}: ').strip()
            if chosen_word == '':
                print("Enter a word!\n")
            else:
                for char in chosen_word:
                    if char in invalid_value[0] or char in invalid_value[1]:
                        identified_invalid.add(char)
                if len(identified_invalid) == 0:
                    invalid = False
                else:
                    print(f"Invalid input. Special digits '{', '.join(identified_invalid)}' are not allowed!\n")

        user_input.append(chosen_word)

    add = range(1, len(story))
    story_list = story.split('@')
    for index, word in enumerate(user_input):
        story_list.insert(index + add[index], f'"{word}"')
    completed_story = ''.join(story_list)

    clear_console()
    print(f'\nHere is your confusing story!\n')
    # print line with proper length
    proper_length = 80
    line = ''
    escape_char = '#'
    completed_story += escape_char
    count = 0
    for letter in completed_story:
        if count <= proper_length:
            line += letter
            count += 1
            if letter == escape_char:
                print(f'\t\t{line[:-1].strip()}\n')
        else:
            if letter == ' ':
                count = 0
                print(f'\t\t{line.strip()}')
                line = ''
            else:
                line += letter


def roll_dice():
    print("Welcome to Roll Dice!")

    while True:
        decision = input('\nEnter now to roll 6-sided dice.\nEnter "x" to quit.\n'
                         'Or enter an integer of desire: ').strip().lower()
        if decision == 'x':
            break
        elif decision == "":
            print(f'6-sided dice --------------------> {random.randint(1, 6)}')
        else:
            # check for integer
            incorrect = True
            while incorrect:
                try:
                    decision = int(decision)
                    if decision < 6:
                        raise ValueError
                    incorrect = False
                except ValueError:
                    print("The number of sides has to be >= 6.")
                    decision = input("Enter a desired integer of sides: ").strip()

            print(f'{decision}-sided dice -------------------> {random.randint(1, decision)}')


def guess_number():
    print('Welcome to Guess the Number!')

    lower = 1
    upper = 100
    mysterious_number = random.randint(lower, upper)
    limit = 7
    print(f'\nYou have {limit} available guesses.')
    print(f'The mysterious number is an integer between {lower} and {upper}.\n')

    count = 1
    guess = upper + 1
    while guess != mysterious_number and count <= limit:
        try:
            guess = int(input(f'Your guess #{count}/{limit}: '))
            if guess < mysterious_number:
                print(f"{guess} is less than the number")
            elif guess > mysterious_number:
                print(f'{guess} is more than the number')
            else:
                break
            count += 1
        except ValueError:
            print('\nYou need to input an integer!')

    if count < limit:
        print("\nCongratulations, you win!")
    else:
        if guess == mysterious_number:
            print("\nCongratulations, you win!")
        else:
            print("\nYou LOSE!")
    print(f'The mysterious number is {mysterious_number}.\n')


# Not game functions ---------------------------------------------------------------------------------------------------

def replay(game_function):

    # Games that don't need to be replayed or can be replayed by its own game function are in exception list.
    exception = [roll_dice]
    if game_function in exception:
        return

    final_decision = input("Enter ---> replay.\n"
                           "Enter 'x' ---> return to game selection.\n"
                           "Enter your decision: ").strip().lower()
    if final_decision == "":
        clear_console()
        game_function()


def clear_console():
    os.system('cls')


def quit_game():
    input('\nPress Enter to continue... ')


def handle_decision(all_games) -> str:
    # get and check decision
    decision = ''
    while decision not in all_games.keys():
        decision = input("Enter a game number: ").strip()
        if decision == 'x':
            return decision
        if decision not in all_games.keys():
            print("-----> Invalid game number\n")
    return decision


def print_intro(all_games):
    print("\nAll available games:")
    for num, (title, function) in sorted(all_games.items()):
        print(f'{num}: {title}')
    print('Enter "x" to exit.\n')


# main structure -------------------------------------------------------------------------------------------------------

def main():
    # all_games = {key: (game title, game function)}
    all_games = game_info()

    while True:

        print_intro(all_games)
        decision = handle_decision(all_games)
        if decision == 'x':
            break

        # call the selected game function
        clear_console()
        all_games[decision][1]()
        replay(all_games[decision][1])
        quit_game()
        clear_console()

    # quit entire program
    print("\nThank you for playing!\nSee you next time. xd")
    time.sleep(5)


main()