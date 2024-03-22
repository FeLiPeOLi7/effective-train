def revert():
    s = input("Put a string that you want to revert: ")
    a = s.split()
    a.reverse()
    print(' '.join(a))

if __name__ == "__main__":
    revert()

