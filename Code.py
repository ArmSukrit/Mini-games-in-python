import random
import time
import os
from random_word import RandomWords
import webbrowser as web


def problems_or_nice_features():
    """
    - getpass() does not seem to work
    - in multiplayer games, winner announcement should be good looking, ex: use big emoji with winner's name/icon
    """


# do not forget to manually add new game's info into this function which acts as database
def game_info() -> dict:
    return {
        '1': ('Guess the Number', guess_number),
        '2': ('Roll a dice', roll_dice),
        '3': ('Confusing Stories', confusing_stories),
        '4': ('Rock Paper Scissors', rock_paper_scissors),
        '5': ('Hangman (requires internet connection)', hangman),
        '6': ('4 In A Row (requires 2 players)', four_in_a_row),
    }


# Every game function --------------------------------------------------------------------------------------------------

def four_in_a_row():
    clear_console()
    print("Welcome to 4 In A Row!\n")

    def print_table():
        # print table for players to see
        table_to_print = ''
        for row_to_print in table:
            table_to_print += '        |'
            times = 0
            for each_element in row_to_print:
                if times < 9:
                    table_to_print += f' {each_element} |'
                else:
                    table_to_print += f' {each_element}  |'
                times += 1
            table_to_print += '\n'
        table_to_print += f'\ncolumn:   {"   ".join(columns)}'
        print(f'{table_to_print}\n')

    def get_player_decision():
        while True:
            player_decision = input(f'Player "{players[player_order[index]]}" chooses column: ')
            if player_decision == 'x':
                return player_decision
            if player_decision not in columns:
                print(f'Possible columns are {" ".join(columns)} only!\n')
            else:
                return player_decision

    # print rules
    print(
        'Rules:\n'
        "\t2 players have to take turns to choose a column to drop a coin\n"
        "\tIf whose every 4 coins align in a horizontal, diagonal or vertical line, that player wins.\n"
    )

    # table creation
    row = 6
    column = 7
    # select table size
    while True:
        decision = input(
            'Do you want to create a bigger table? --> default is (row = 6 x column = 7)\n'
            'With customization, row >= 6 and column >= 7\n'
            '(y, n)?: '
        )
        if decision not in 'yn':
            print('Choose y or n.')
        else:
            break
    if decision == 'y':
        while True:
            try:
                row = int(input('Number of rows: ').strip())
                if row < 6:
                    raise FileNotFoundError
                column = int(input('Number of columns: ').strip())
                if column < 7:
                    raise ArithmeticError
                break
            except FileNotFoundError:
                print('Number of rows has to be >= 6!')
            except ArithmeticError:
                print('Number of columns has to be >= 7!')
            except ValueError:
                print('Enter only an integer!')
    # create table for real
    table = []
    blank = '_'
    for i in range(row):
        each_row = []
        for k in range(column):
            each_row.append(blank)
        table.append(each_row)
    # possible columns
    columns = [str(i + 1) for i in range(column)]
    stack_limit = row

    # create players
    print()
    index = 1
    player_order = (1, 2)
    icon1 = ''
    icon2 = icon1
    while icon1 == icon2:
        while True:
            icon1 = input(f'First player, choose your representative icon (cannot be "{blank}"): ').strip()
            if len(icon1) != 1:
                print('Only one character!')
            elif icon1 == blank:
                print(f'Not "{blank}"')
            else:
                break
        while True:
            icon2 = input(f'Second player, choose your representative icon (cannot be "{blank}"): ').strip()
            if len(icon2) != 1:
                print('Only one character!')
            elif icon2 == blank:
                print(f'Not "{blank}"')
            else:
                break
        if icon1 == icon2:
            print('Cannot use the same icon!\n')

    players = {1: icon1, 2: icon2}

    # game start
    final_decision = ''
    while True:
        clear_console()
        # print table for players to see
        print_table()

        # coin drop process
        row_to_replace = row - 1
        if index == 0:
            index = 1
        else:
            index = 0
        # get player decision
        while True:
            player_choose_column = get_player_decision()
            if player_choose_column == 'x':
                final_decision = input('Are you sure you want to restart or exit now?\n'
                                       '(y, n)?: ')
                if final_decision == 'y':
                    break
            else:
                break
        if final_decision == 'y':
            print()
            break

        # drop in table
        target = table[row_to_replace][int(player_choose_column) - 1]
        while True:
            if target == blank:
                table[row_to_replace][int(player_choose_column) - 1] = players[index + 1]
                break
            else:
                row_to_replace -= 1
                try:
                    target = table[row_to_replace][int(player_choose_column) - 1]
                except IndexError:
                    print(f'Each stack in a column cannot go over {stack_limit}. Try another column\n')
                    # get player decision again until valid
                    player_choose_column = get_player_decision()

        # check for winning condition
        winner = 0
        winner_found = False
        alignment = None

        # horizontal
        i = 0
        for each_row in table:
            count = 1
            for i in range(len(each_row)):
                try:
                    if each_row[i] == each_row[i + 1] and each_row[i] != blank:
                        count += 1
                        if count == 4:
                            break
                    else:
                        count = 1
                except IndexError:
                    pass
            if count == 4:
                winner_found = True
                alignment = 'horizontal'
                winner = each_row[i]
                break

        # vertical
        if not winner_found:
            column_to_check = 0
            count = 1
            for e in range(column):
                for i in range(row):
                    try:
                        if table[i][column_to_check] == table[i + 1][column_to_check] and \
                                table[i][column_to_check] != blank:
                            count += 1
                            if count == 4:
                                winner_found = True
                                alignment = 'vertical'
                                winner = table[i][column_to_check]
                                break
                        else:
                            count = 1
                    except IndexError:
                        pass
                    if i == row - 1:
                        column_to_check += 1
                if winner_found:
                    break

        # diagonal
        if not winner_found:
            # "backward" diag check
            for i in range(row):
                for k in range(column):
                    try:
                        left1 = table[i][k]
                        left2 = table[i + 1][k + 1]
                        right1 = table[i + 2][k + 2]
                        right2 = table[i + 3][k + 3]
                        if left1 == left2 == right1 == right2 and left1 != blank:
                            winner_found = True
                            winner = left1
                            alignment = 'backward diagonal'
                            break
                    except IndexError:
                        pass
                if winner_found:
                    break
            # "forward" diag check
            if not winner_found:
                for i in range(row):
                    for k in range(column):
                        try:
                            left1 = table[i][k]
                            left2 = table[i - 1][k + 1]
                            right1 = table[i - 2][k + 2]
                            right2 = table[i - 3][k + 3]
                            if left1 == left2 == right1 == right2 and left1 != blank:
                                winner_found = True
                                winner = left1
                                alignment = 'forward diagonal'
                                break
                        except IndexError:
                            pass
                    if winner_found:
                        break

        # check if table is fully filled
        draw = True
        for row in table:
            if blank in row:
                draw = False
                break

        # announcement
        if winner_found:
            clear_console()
            print_table()
            print(f'The winner is player {winner}!!! \n'
                  f'({alignment}, with last column = {player_choose_column})\n')
            break
        if draw:
            clear_console()
            print_table()
            print(f'Table is fully filled.\n'
                  f'DRAW!!!\n')


def hangman():
    clear_console()
    print("Welcome to Hangman!")

    a = '---> word length ='
    difficulty = {
        '1': (f'easy {a} 5 or 6', random.randint(5, 6)),
        '2': (f'normal {a} 7, 8 or 9', random.randint(7, 9)),
        '3': (f'hard {a} 10 or more', None),
        '4': (f'random {a} between 5 and 10', random.randint(5, 10),)
    }
    print('\nDifficulty levels: ')
    for key, value in sorted(difficulty.items()):
        print(f'{key}: {value[0]}')

    # input filter
    while True:
        chosen_difficulty = input("Choose difficulty: ")
        if chosen_difficulty not in difficulty.keys():
            print(f'\nChoose {", ".join(difficulty.keys())} only!')
        else:
            break

    # hint at final guess with 30% chance
    hint_active = False
    if random.randint(1, 10) in {1, 2}:
        hint_active = True

    # words selection
    word_generator = RandomWords()
    number_of_words = 10

    word_length = difficulty.get(chosen_difficulty, random.randint(5, 10))[1]
    while True:
        # gather random words
        while True:
            clear_console()
            print("\nGathering words... (If this takes too long, check your internet connection.)")
            try:
                if word_length is not None:
                    random_words = word_generator.get_random_words(
                        limit=number_of_words, minLength=word_length, maxLength=word_length
                    )
                else:
                    random_words = word_generator.get_random_words(
                        limit=number_of_words, minLength=10
                    )
                break
            except:
                print("\nConnection error detected.\nHangman needs stable internet connection.\nTry again?.")
                while True:
                    final_decision = input("(y, n)?: ").strip().lower()
                    if final_decision in ['y', 'n']:
                        break
                if final_decision == 'n':
                    clear_console()
                    main()

        random_words = [word.lower() for word in random_words]
        # filter any word which contains non-alphabetical out
        for word in random_words:
            remove = False
            for alphabet in word:
                if not 'a' <= alphabet <= 'z':
                    remove = True
            if remove:
                random_words.remove(word)

        print(f'The word is one of these: \n\n\t{", ".join(random_words[:len(random_words)//2])}\n'
              f'\t{", ".join(random_words[len(random_words)//2:])}\n')
        decision = input("Random a new word set ---> Enter 'x'\n"
                         "             To start ---> Press Enter!\n"
                         "(x, Enter)? : ")
        if decision != 'x':
            break
    clear_console()

    full_body = {
        'hanger': '_________________\n'
                  '                |\n'
                  '                |',
        'head': '              (T_T)',
        'neck': '                |',
        'arms': '              \ | / \n'
                '               \|/ ',
        'body': '                |\n'
                '                |',
        'legs': '               / \ \n'
                '              /   \ ',
        'feet': '            __     __'
    }
    hang_order = ('hanger', 'head', 'neck', 'arms', 'body', 'legs', 'feet')

    mysterious_word = random_words[random.randint(0, len(random_words) - 1)]
    mysterious_word_to_report = mysterious_word[:]
    mysterious_word = list(mysterious_word)
    length = len(mysterious_word)
    blank_spaces = list('_' * length)
    guess_limit = len(full_body.keys())
    alphabets = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
    you_have_guessed = []
    body = []

    # inform word's info
    print(f'\nThe mysterious word is among these: \n\n\t{", ".join(random_words[:len(random_words)//2])}\n'
          f'\t{", ".join(random_words[len(random_words)//2:])}\n')
    input('Press Enter to continue...')

    # main game sequence
    hang_order_index = 0
    while True:

        clear_console()
        if guess_limit != 1:
            print(f"{guess_limit} guesses left.")
        else:
            print("DECISIVE GUESS...")
            if hint_active:
                print(f'HINT!!! (20% chance)\nThe word is one of these: \n\n\t{", ".join(random_words)}\n')
                hint_active = False
        print(f"You haven't guessed: {' '.join(alphabets)}")
        if you_have_guessed:
            print(f"You have guessed: {' '.join(you_have_guessed)}")
        print(f'\n\t\t\t\t{" ".join(blank_spaces)}')
        # body printing
        for body_part in body:
            print(body_part)

        # check whether win or lose
        if set(mysterious_word) == {''}:
            print(f"\nCongratulations! YOU WIN!!!.\nThe mysterious word is indeed '{mysterious_word_to_report}'.\n")
        else:
            if guess_limit == 0:
                print(f"\nYOU LOSE!!!\nThe mysterious word is {mysterious_word_to_report}.\n")
        if set(mysterious_word) == {''} or guess_limit == 0:
            while True:
                see_translation = input(f"Do you want to see translation in Thai for '{mysterious_word_to_report}'?\n"
                                        "(y, n)?: ").strip().lower()
                if see_translation not in 'yn':
                    print("Enter y or n.\n")
                else:
                    print()
                    break
            if see_translation == 'y':
                web.open(
                    f'https://translate.google.com/#view=home&op=translate&sl=en&tl=th&text={mysterious_word_to_report}'
                )
            break

        # guess check
        while True:
            guess = input("Your guess: ").strip().lower()
            if not 'a' <= guess <= 'z':
                print('You can guess an alphabet only!')
            else:
                if len(guess) > 1:
                    print('One character only!')
                else:
                    if guess in you_have_guessed:
                        print(f'You have already guessed "{guess}"')
                    else:
                        break

        # game mechanism
        you_have_guessed.append(guess)
        if guess in mysterious_word:
            # reform mysterious_word and black_spaces
            new_mysterious_word = []
            new_black_spaces = blank_spaces.copy()
            for index, char in enumerate(mysterious_word):
                if guess == char:
                    new_mysterious_word.append("")
                    new_black_spaces[index] = guess
                else:
                    new_mysterious_word.append(char)
                    if guess not in you_have_guessed:
                        new_black_spaces[index] = '_'
            mysterious_word = new_mysterious_word
            blank_spaces = new_black_spaces

            alphabets.remove(guess)
        else:
            alphabets.remove(guess)
            guess_limit -= 1
            body.append(full_body[hang_order[hang_order_index]])
            hang_order_index += 1


def rock_paper_scissors():
    clear_console()
    print("Welcome to Rock Paper Scissors!")
    print('Choose "x" to return to game selection.\n')

    rock = 'rock'
    paper = 'paper'
    scissors = 'scissors'
    possibilities = {'1': rock, '2': paper, '3': scissors}
    mode = {'1': '1 player VS computer', '2': 'player 1 VS player 2'}
    players = [
        ['You', 'Computer'],
        ['Player 1', 'Player 2']
    ]

    # mode selection
    single_player = True
    print('Modes:')
    for mode_key, mode_detail in sorted(mode.items()):
        print(f'{mode_key}: {mode_detail}')
    while True:
        selected_mode = input(f'(1, 2)?: ').strip()
        if selected_mode in mode.keys():
            break
        else:
            print('Choose either 1 or 2.\n')
    if selected_mode != '1':
        single_player = False
    clear_console()

    while True:
        # inform what can be chosen
        inform = ''
        for key, value in sorted(possibilities.items()):
            inform += f'{key} = {value}\t'
        print(inform + ' ----------> x to stop')

        # first input filter
        while True:
            if single_player:
                player1_chooses = input(f'{players[0][0]}: ').strip().lower()
            else:
                player1_chooses = input(f'{players[1][0]}: ').strip().lower()
                clear_console()
                inform = ''
                for key, value in sorted(possibilities.items()):
                    inform += f'{key} = {value}\t'
                print(inform + ' ----------> x to stop')
            if player1_chooses == 'x':
                break
            if player1_chooses not in possibilities.keys():
                print('Choose 1, 2 or 3.\n')
            else:
                break
        if player1_chooses == 'x':
            break
        # second input filter, if there is.
        if single_player:
            player2_chooses = str(random.randint(1, 3))
        else:
            while True:
                player2_chooses = input(f'{players[1][1]}: ').strip().lower()
                if player2_chooses == 'x':
                    break
                if player2_chooses not in possibilities.keys():
                    print('Choose 1, 2 or 3.\n')
                else:
                    break
        if player2_chooses == 'x':
            break

        player1_chooses = possibilities[player1_chooses]
        player2_chooses = possibilities[player2_chooses]

        # report result process
        clear_console()
        if single_player:
            report = f'{players[0][0]}: {player1_chooses} VS {players[0][1]}: {player2_chooses} ---> '
        else:
            report = f'{players[1][0]}: {player1_chooses} VS {players[1][1]}: {player2_chooses} ---> '
        lose = 'YOU LOSE!'
        draw = 'DRAW!!!'
        if player1_chooses == player2_chooses:
            report += draw
        else:
            if player1_chooses == rock:
                if player2_chooses == paper:
                    if single_player:
                        report += lose
                    else:
                        report += f'PLAYER 2 WINS!'
                else:
                    if single_player:
                        report += 'YOU WIN!'
                    else:
                        report += f'PLAYER 1 WINS!'
            elif player1_chooses == paper:
                if player2_chooses == scissors:
                    if single_player:
                        report += lose
                    else:
                        report += 'PLAYER 2 WINS!'
                else:
                    if single_player:
                        report += 'YOU WIN!'
                    else:
                        report += 'PLAYER 1 WINS!'
            else:
                if player2_chooses == rock:
                    if single_player:
                        report += lose
                    else:
                        report += 'PLAYER 2 WINS!'
                else:
                    if single_player:
                        report += 'YOU WIN!'
                    else:
                        report += 'PLAYER 1 WINS!'

        report += '\n'
        print(report)


def confusing_stories():
    clear_console()
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
            'Yesterday, @ and I went to the park. On our way to the @ park, we saw a @ @ on our bike. '
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
                print(f'\t{line[:-1].strip()}\n')
        else:
            if letter == ' ':
                count = 0
                print(f'\t{line.strip()}')
                line = ''
            else:
                line += letter


def roll_dice():
    clear_console()
    print("Welcome to Roll Dice!")

    print('\nEnter now to roll 6-sided dice.\nEnter "x" to quit.\nOr enter an integer to make a custom dice\n')
    while True:
        decision = input("(Enter, integer >= 6)?: ").strip().lower()
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
    clear_console()
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

def print_enter_to_continue():
    input('Press Enter to continue...')


def replay(game_function):
    # Games that don't need to be replayed or can be replayed by its own game function are in exception list.
    exception = [roll_dice, rock_paper_scissors]
    if game_function in exception:
        return

    final_decision = input("Enter ---> replay.\n"
                           "Enter 'x' ---> return to game selection.\n"
                           "(Enter, x)?: ").strip().lower()
    if final_decision == "":
        clear_console()
        game_function()


def clear_console():
    os.system('cls')


def get_input(all_games: dict) -> str:
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


# main structure -------------------------------------------------------------------------------------------------------

def main():
    # all_games = {key: (game title, game function)}
    all_games = game_info()

    while True:

        print_intro(all_games)
        decision = get_input(all_games)
        if decision == 'x':
            break

        # call the selected game function
        clear_console()
        while True:
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


main()
