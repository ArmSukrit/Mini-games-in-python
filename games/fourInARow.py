import sys
sys.path.append("\\Mini-games-in-python\\")
from tools import *


def four_in_a_row():
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
        ).strip().lower()
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
                    row_to_replace = row - 1
                    target = table[row_to_replace][int(player_choose_column) - 1]

        # check for winning condition
        winner = None
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
        for each_row in table:
            if blank in each_row:
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
            break
