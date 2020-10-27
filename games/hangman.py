import random
import time
from random_word import RandomWords  # pip install random-word
import webbrowser as web
# from

import sys
sys.path.append("\\Mini-games-in-python\\")
from tools import *


def hangman():
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
    limit = 10
    active = True
    while active:
        # gather random words
        i = 1
        random_words = []
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
                if random_words:
                    break
            except:
                print(f'{i}/{limit} Retrying...')
                if i == limit:
                    final_decision = input(
                        f'{i} seconds have passed. Would you like to try again or go back to menu?\n'
                        f'(t: try again, x: quit)?: ').strip().lower()
                    if final_decision in ('t', 'try', 'try again'):
                        i = 0
                    else:
                        clear_console()
                        active = False
                        break
                i += 1
                time.sleep(1)

        if not active:
            break

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

    if active:
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
        blank = '_'
        blank_spaces = list(blank * length)
        guess_limit = len(full_body.keys())
        alphabets = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()
        you_have_guessed = []
        body = []

        # inform word's info
        print(f'\nThe mysterious word is among these: \n\n\t{", ".join(random_words[:len(random_words)//2])}\n'
              f'\t{", ".join(random_words[len(random_words)//2:])}\n')
        print_enter_to_continue()

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
                            new_black_spaces[index] = blank
                mysterious_word = new_mysterious_word
                blank_spaces = new_black_spaces

                alphabets.remove(guess)
            else:
                alphabets.remove(guess)
                guess_limit -= 1
                body.append(full_body[hang_order[hang_order_index]])
                hang_order_index += 1
