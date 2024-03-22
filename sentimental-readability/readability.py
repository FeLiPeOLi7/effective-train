# TODO
from cs50 import get_string

text = get_string("Put some text here: ")
letter_counter = 0
word_counter = 1
sentence_counter = 0

i = 0
for i in range(len(text)):
    if text[i] >= 'a' and text[i] <= 'z' or text[i] >= 'A' and text[i] <= 'Z':
        letter_counter += 1
    elif text[i] == ' ':
        word_counter += 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentence_counter += 1

L = (letter_counter / word_counter) * 100
S = (sentence_counter / word_counter) * 100
grade = round((0.0588 * L) - (0.296 * S) - 15.8)
if grade < 16 and grade >= 0:
     print(f"Grade is {grade}")
elif grade >= 16:
    print("Grade 16+")
else:
    print("Before Grade 1")