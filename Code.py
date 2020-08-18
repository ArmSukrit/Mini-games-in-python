import random
import time


# Every game function

def confusing_stories():
    print('\n' * 5 + "Welcome to Confusing Stories!")
    # story_templates = {key: (title, number of required, input words, story)}
    # '@' is meant to be replaced with user_input
    stories = {
        '1': (
            'Spring Cartoon!',
            10,
            'noun/s.adj.noun.noun/s.noun/s.noun.type of food.noun/s.noun.adjective',
            'Planting a vegetable garden is not only fun, it also helps save @. You will need a piece of @ '
            'land. You may need a @ to keep the @ and @ out. As soon as @ is here you can go out there with '
            'your @ and plant all kinds of @. Then in a few months, you will have corn on the @ and big, @ '
            'flowers.'),
    }

    # inform about stories
    print('\nAll available stories:')
    for key, value in sorted(stories.items()):
        print(f'{key}: {value[0]}  {value[1]} words are required.')

    # get and check input
    decision = ''
    while decision not in stories.keys():
        decision = input('Enter a story number: ').strip()
        if decision not in stories.keys():
            print('-----> Invalid story number.\n')

    # main game sequence
    title, num, input_words, story = stories[decision]
    required_words = input_words.split('.')
    user_input = []

    for num, each in enumerate(required_words, 1):
        user_input.append(input(f'{num}/{len(required_words)} Enter {each}: '))

    add = range(1, len(story))
    story_list = story.split('@')
    for index, word in enumerate(user_input):
        story_list.insert(index + add[index], word)
    completed_story = ''.join(story_list)

    # chop completed_story into readable lines with proper line length
    proper_length = 200
    count = 1
    lines = []
    each_line = ''
    for letter in completed_story:
        each_line += letter
        count += 1
        if count >= proper_length or letter == completed_story[-1]:
            if letter == '.' and letter != completed_story[-1]:
                pass
            else:
                lines.append(each_line.strip())
                each_line = ''
                count = 0

    print(f'\nHere is your story:\n')
    for line in lines:
        print(f'\t\t{line}')

    quit_game()


def roll_dice():
    print('\n' * 5 + "Welcome to Roll Dice!")
    while True:
        decision = input('\nEnter now to roll 6-sided dice.\nEnter "x" to quit.\n'
                         'Or enter an integer of desire: ').strip().lower()
        if decision == 'x':
            print('\n' * 5)
            break
        elif decision == "":
            print(f'6-sided dice ------> {random.randint(1, 6)}')
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
                    print("The number of sides must be an integer and greater than 5.")
                    decision = input("Enter a desired integer of sides: ").strip()

            print(f'{decision}-sided dice ------> {random.randint(1, decision)}')


def guess_number():
    print('\n' * 5 + 'Welcome to Guess the Number!')

    lower = 1
    upper = 100
    mysterious_number = random.randint(lower, upper)
    limit = 7
    print(f'\nYou have {limit} available guesses.')
    print(f'The mysterious number is an integer between {lower} and {upper}.\n')

    count = 1
    guess = range(lower, upper)[-1] + 1
    while guess != mysterious_number and count <= limit:
        guess = int(input(f'Your guess #{count}: '))
        if guess < mysterious_number:
            print(f"{guess} is less than the number")
        elif guess > mysterious_number:
            print(f'{guess} is more than the number')
        else:
            break
        count += 1

    if count < limit:
        print("\nCongratulations, you win!")
    else:
        if guess == mysterious_number:
            print("\nCongratulations, you win!")
        else:
            print("You LOSE!\n")
    print(f'The mysterious number is {mysterious_number}.\n')

    quit_game()


def quit_game():
    input('\nPress Enter to continue: ')
    print('\n\n\n\n\n')


# Not game functions

def handle_decision(all_games) -> str:
    # get and check decision
    decision = ''
    while decision not in all_games.keys():
        decision = input("Enter a game number: ").strip()
        if decision not in all_games.keys():
            print("-----> Invalid game number\n")
        if decision == 'x':
            return decision
    return decision


def print_intro(all_games):
    print("\nAll available games:")
    for num, (title, function) in sorted(all_games.items()):
        print(f'{num}: {title}')
    print('Enter "x" to exit.\n')


# main structure
def main():
    # do not forget to manually add new game's info to this dictionary
    # all_games = {key: (game's title, game's function)}
    all_games = {
        '1': ('Guess the Number', guess_number),
        '2': ('Roll a dice', roll_dice),
        '3': ('Confusing Stories', confusing_stories),
    }

    while True:

        print_intro(all_games)
        decision = handle_decision(all_games)
        if decision == 'x':
            break

        # run the selected game
        all_games[decision][1]()

    print("Thank you for playing!\nSee you next time. xd")
    time.sleep(5)


main()
