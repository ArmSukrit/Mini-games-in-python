import random


def roll_dice():
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
