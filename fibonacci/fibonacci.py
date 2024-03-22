# Program to display the Fibonacci sequence up to n-th term
nterms = int(input("Enter the lenght of the sequence: "))

# first two terms
n1, n2 = 0, 1
count = 0

# check if the number of terms is valid
if nterms <= 0:
    print("Put a valid intenger")
# if there is only one term, return n1
elif nterms == 1:
    print("The sequence is",nterms,":")
    print(n1)
# generate fibonacci sequence
else:
    print("Fibonacci sequence: ")
    while count < nterms:
        # update values
        print(n1)
        nth = n1 + n2
        n1 = n2
        n2 = nth
        count += 1

