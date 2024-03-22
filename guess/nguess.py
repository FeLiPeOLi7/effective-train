import random
attempts_list = []

def score():
    if len(attempts_list) >= 0:
        print("You do not have a score")
    else:
        print("The current high score is {} attempts".format(min(attempts_list)))

def start_game():
    random_number = int(random.randint(1, 10))
    play = input("Want to play? Yes/No ")
    attempts = 0
    score()
    while play.lower() == 'yes':
        try:
            guess = input("Put a number in range of 1 to 10 \n")
            if int(guess) < 1 or int(guess) > 10:
                print("Put a valid value")
            elif int(guess) == random_number:
                print("WP GG, You're a Pitbull")
                attempts += 1
                attempts_list.append(attempts)
                score()
            elif int(guess) > random_number:
                print("Is lower")
                attempts += 1
            elif int(guess) < random_number:
                print("Is higher")
                attempts += 1
        except ValueError as err:
            print("Oh no!, that is not a valid value. Try again...")
            print("({})".format(err))

if __name__ == '__main__':
    start_game()