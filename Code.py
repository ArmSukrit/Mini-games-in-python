import random
import time


# do not forget to manually add new game's info to this dictionary
# all_games = {key: (game's title, game's function)}
all_games = {
  '1': ('Guess the number', Guess_Number()),
  '2': ('Roll a dice', Roll_Dice()),
  '3': ('Confusing Stories', Confusing_Stories()),
}
  
  
# Every game function

def Confusing_Stories():
  # story_templates = {key: (title, input words, story)}, '@' is meant to be replaced with user_input
  stories = {
    '1': (
      'Spring Cartoon!',
      'noun/s.adj.noun.noun/s.noun/s.noun.type of food.noun/s.noun.adjective',
      'Planting a vegetable garden is not only fun, it also helps save @. You will need a piece of @ land. You may need a @ to keep the @ and @ out. As soon as @ is here you can go out there with your @ and plant all kinds of @. Then in a few mounths, you will have corn on the @ and big, @ flowers.'),
  }
  
  # inform about stories
  print('All available story:\n')
  for key, value in sorted(stories.items()):
    print(f'{key}: {value[0]}')
    
  # get and check input
  decision = ''
  while decision not in stories.keys():
    decision = intput('Enter a story number: \n').strip()
    if decision not in stories.keys():
      print('Invalid story number.')
  
  # main game sequence
  title, input_words, story = stories[decision]
  required_words = input_words.split('.')
  user_input = []
  
  for each in required_words:
    user_input.append(input(f'Enter {each}: '))
    
  add = range(1, len(story))  
  story_list = story.split('@')
  for index, word in enumerate(user_input):
    story_list.insert(index + add[index], word)
  completed_story = story_list.join('')
  
  print(f'\nHere is your story:\n\t{completed_story}\n')
  quit_game()
  

def Roll_Dice():
  number_of_sides = 6
  while True:
    decision = input('Enter now to roll 6-sided dice.\nEnter "x" to quit.\nOr enter an integer of desire: ').strip().lower()
    if decision == 'x':
      break
    elif decision == "":
      print(f'6-sided dice -> {random.randint(1, 6)}')
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
      
      print(f'{decision}-sided dice -> {random.randint(1, decision)}\n')
  

def Guess_Number():
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
    print("Congratulations, you win!\n")
    print(f'The mysterious number is {mysterious_number}.\n')
  else:
    if guess == mysterious_number:
      print("Congratulations, you win!\n")
    else:
      print("You LOSE!\n")
  quit_game()
  
  
def quit_game():
  input('Press Enter to continue')
  
  
# Not game functions

def print_intro():
  print("All available games:")
  for num, (title, function) in sorted(all_games.items()):
    print(f'{num}: {title}')
  print('Enter "x" to exit.\n')
  
  
# main structure
while True:
  
  print_intro()
  
  # get and check decision
  decision = ''
  while decision not in all_games.keys():
    decision = input("Enter a game number: ").strip()
    if decision not in all_games.keys():
      print("Invalid game number")
    if decision == 'x':
      break
  
  # run the selected game
  all_games[decision][1]
  
print("Thank you for playing!\nSee you next time. xd")
time.sleep(5)
