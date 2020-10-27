import random

import sys
sys.path.append("\\Mini-games-in-python\\")
from tools import *


def rock_paper_scissors():
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
