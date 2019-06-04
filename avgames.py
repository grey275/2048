import sys
import random as rd
import numpy as np
from game import *
board = None

def randmove():
    rd.seed()
    moves = avmoves(board)
    if moves:
        return rd.choice(moves)

scores = []
low = 1000
high = 0
index = 0
print(sys.argv[1])
while index < int(sys.argv[1]):
    global score, ssind
    board = np.zeros((4,4))
    genseed(False)
    g = gamestart(randmove, False, board)[0]
    scores.append(g)
    print('game %d completed' % (index))
    if g < low:
        low = g
    elif g > high:
        high = g
    index += 1
avscore = sum(scores)/len(scores)
print("The average score of %s randomly generated games is %d/n The highest score was %d and the lowest was %d" % (len(scores), avscore, high, low))
