from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

my_bot = ChatBot(name ="PyBot", read_only=True, logic_adapters=
['chatterbot.logic.MathematicalEvalution', 'chatterbot.logic.BestMatch'])

small_talk = ['hi', 'hi there', 'how are you?', 'Im fine thanks to ask', 'whats you name?',
'my name is PyBot, ask a math question']

math_talk1 = ['Pythagorean theorem',
'a squared plus b squared equal c squared.'
]

math_talk2 = ['Cos law',
'c**2 = a**2 + b**2 - 2*a*b*cos(alpha)'
]

list_trainer = ListTrainer(my_bot)

for item in(small_talk, math_talk1, math_talk2):
    list_trainer.train(item)