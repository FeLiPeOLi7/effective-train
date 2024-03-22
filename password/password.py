import string
import random

alphabet = list(string.ascii_letters)
digits = list(string.digits)
special = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate():
    while True:
        password_lenght = int(input("Put the lenght of the password: "))

        alphabet_count = int(input("Put how many normal character you want: "))
        digit_count = int(input("Put how many digits you want: "))
        special_count = int(input("Put how many special character you want: "))

        characters_count = alphabet_count + digit_count + special_count

        if characters_count > password_lenght:
            another = print(input("Characters total count is higher than the lenght, want to try again? yes/no \n"))
        if another == "no":
            break
        elif another == "yes":
            continue
        else:
            print("Invalid")

        password = list()

        for i in range(alphabet_count):
            password.append(random.choice(alphabet))

        for i in range(digit_count):
            password.append(random.choice(digits))

        for i in range(special_count):
            password.append(random.choice(special))

        if password_lenght < characters_count:
            random.shuffle(characters)
        for i in range(password_lenght):
            password.append(random.choice(characters))

        random.shuffle(password)

        print("".join(password))


generate()