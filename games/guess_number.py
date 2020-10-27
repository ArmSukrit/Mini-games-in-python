import random


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
