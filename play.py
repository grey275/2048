import sys, os
from game import *
board = None

def playerinput():
    keylist = "wasdrx"
    while True:
        key = ms.getch().decode()
        for i, k in enumerate(keylist):
            if key == k:
                print(i)
                return i
        print("Invalid character. Valid keys are: "+keylist)

def restart():
    global board, score
    board = None
    score = 0
    print('game restarted')

try:
    seedget(sys.argv[1], os.listdir('seeds'))

except IndexError:
    print('IE')
    genseed()

while True:
    board = np.zeros((4,4))
    gameout = gamestart(playerinput, viewboard, board)
    print('Game over. Final score is %s.' % gameout[1])
    if not gameout[1]:
        print('Press any key to restart or x to quit')
        if playerinput() == 5:
            quit()
    elif gameout[1] == 5:
        quit()
