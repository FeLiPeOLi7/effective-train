# Program make a simple calculator

# This function adds two numbers
def add(x, y):
    return x + y

# This function subtracts two numbers
def subtract(x, y):
    return x - y

# This function multiplies two numbers
def multiply(x, y):
    return x * y

# This function divides two numbers
def divide(x, y):
    return x / y

# This function exponentiate two numbers
def expo(x, y):
    return x ** y

# This function radicilizate two numbers
def rad(x, y):
    return x ** 1/y

# Propagação de incerteza
def incerteza(x, y, sx, sy):
    g = x / y
    sg = g * (0.5 ** (((sx / x) ** 2) + ((sy / y) ** 2)))
    return sg


print("Select operation.")
print("1.Add")
print("2.Subtract")
print("3.Multiply")
print("4.Divide")
print("5.Exponentiate")
print("6.Radicialização")
print("7.Propagação de incerteza")

while True:
    # take input from the user
    choice = input("Enter choice(1/2/3/4/5/6/7): ")

    # check if choice is one of the four options
    if choice in ('1', '2', '3', '4', '5', '6'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    elif choice in ('7'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        sx = float(input("Put the X doubt:"))
        sy = float(input("Put the y doubt:"))

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))

        elif choice == '5':
            print(num1, "^", num2, "=", expo(num1, num2))

        elif choice == '6':
            print(num1, "sqr", num2, "=", rad(num1, num2))

        elif choice == '7':
            print(num1, "*", num2, "=", incerteza(num1, num2, sx, sy))

        # check if user wants another calculation
        # break the while loop if answer is no
        next_calculation = input("Let's do next calculation? (yes/no): ")
        if next_calculation == "no":
          break

    else:
        print("Invalid Input")

