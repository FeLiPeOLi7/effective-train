import random

while True:
    print("Come play rock, paper and scisors!")
    userChoice = input("Choose [R]ock, [P]aper or [S]cissors: ")
    choices = ['R', 'S', 'P']
    if not userChoice == choices:
        print("Use a valid weapon")
        continue
    print(f"You chose {userChoice}, nice job")
    opponentChoice = random.choice(choices)

    if opponentChoice == str.upper(userChoice):
        print("Tie!")
    elif opponentChoice == 'R' and str.upper(userChoice) == 'S':
        print("The bot has win")
        continue
    elif opponentChoice == 'S' and str.upper(userChoice) == 'P':
        print("The bot has win")
        continue
    elif opponentChoice == 'P' and str.upper(userChoice) == 'R':
        print("The bot has win")
        continue
    else:
        print("I win")

