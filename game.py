import random as rd
import numpy as np
import sys, os

score = 0
#seed used to generate numbers deterministically
gameseed = None
#keeps track of what numbers have been used from the seed
ssind = 0


#generates either a 1(2 onscreen) or a 2(4 onscreen) and passes it to placenum()
def newnum(b):
    if seeduse(1) == 0:
        num = 2
    else:
        num = 1
    placenum(num, b)

#puts its argument in an empty space on the board
def placenum(num, b):
    empties = []
    for ri, r in enumerate(b):
        for ci, c in enumerate(r):
            if c == 0:
                empties.append((ri, ci))
    rd.seed(seeduse(10))
    rand = rd.choice(empties)
    b[rand] = num

#Generates specified number of ints using gameseed. If the seed has already all been used we use it on itself to increase length.
def seeduse(nints):
    global gameseed, ssind

    if len(gameseed) <= ssind:
        ssind = 0

    nseed = int(gameseed[ssind:ssind+nints])
    ssind += nints
    return nseed

#Saves gameseed to file seeds with the last character of the name being its index in the file.
def saveseed(sdir):
    global gameseed
    newname = 'seed%d' % (int(sdir[-1][-5])+1)
    newpath = 'C:/code/2048/seeds/%s.txt' % (newname)
    with open(newpath, 'w') as savef:
        savef.write(gameseed)
    print("seed saved as %s" % (newname))

#generates new gameseed randomly
def genseed(v=True):
    global gameseed
    if v:
        print("No seed specified. Generating new seed...")
    rd.seed()
    gameseed = str(rd.getrandbits(4096))
    if v:
        print("Completed.")

#based on command line argument it either attempts to retreive seed from the specified file, generates and saves seed, or generates without saving
def seedget(inpseed, sdir):
    global gameseed
    if inpseed == 's':
        genseed(True)
        saveseed(sdir)
    elif inpseed == '!s':
        genseed(False)
    else:
        try:
            with open(sdir + inpseed) as s:
                gameseed = str(s.read())
                print('Seed pulled from %s.' % (inpseed))
        except FileNotFoundError as fnf:
            print(fnf)
            quit()

#Collapses list to the 0 index based on typical 2048 rules.
def collapse(line, sim):
    global score
    nl = []
    #gets rid of spaces and puts resulting list in nl
    for n in line:
        if n != 0:
            nl.append(n)

#Iterates though list, checking if the adjacent value is the same as the current value and adding to one of the values and popping the other one.
    i = 0
    while i < len(nl)-1:
        if nl[i+1] == nl[i]:
            nl[i+1] += 1
            nl.pop(i)
            if not sim:
                score += 1
        else:
            i += 1

#adds back spaces
    empt = len(line) - len(nl)
    nl += [0] * empt

    return nl

#calls collapse normally on rows, which collapses to the left
def swipeleft(b, sim):
    i = 0
    while i < len(b[i]):
        b[i] = collapse(b[i], sim)
        i += 1

#calls collapse on the reverse of the rows
def swiperight(b, sim):
    i = 0
    while i < b[i]:
        b[i] = collapse(b[i,::-1], sim)[::-1]
        i += 1

#Calls collapse  on all columns, aka the nth element of every row.
def swipeup(b, sim):
    i = 0
    while i < len(b):
        col = []

        for r in b:
            col.append(r[i])
        newcol = collapse(col, sim)

        for j,r in enumerate(b):
            r[i] = newcol[j]
        i += 1

#reverse of swipeup
def swipedown(b, sim):
    i = 0
    while i < len(b):
        col = []

        for r in b:
            col.append(r[i])
        newcol = collapse(col[::-1], sim)[::-1]

        for j,r in enumerate(b):
            r[i] = newcol[j]
        i += 1


#displays current boardstate in the console.
def viewboard(b):
    vb = np.copy(b)

    for r in (vb):
        for c in r:
            if c != 0:
                #the board is stored in log base 2 for simplicity so we have to get the actual values
                c = 2**c

    global score
    print(vb)
    print('\nScore: '+ str(score))


#accepts inputs from another function to control the game
def controller(inpfun, b):
    inp = inpfun()

    #checks current board for legal moves
    av = avmoves(b)

    if not av:
        return False

    movcoms = [swipeup, swipeleft, swipedown, swiperight]

    if inp < 4:
        fun = movcoms[inp]
        if inp in av:
           fun(b, False)
           return True
        print('illegal move')
        inp = inpfun()

    return inp


#checks which moves are legal and returns those in a list
def avmoves(b):
    moves = [swipeup, swipeleft, swipedown, swiperight]
    av = []

    for i,s in enumerate(moves):
        sboard = np.copy(b)
        s(sboard, True)
        if not np.array_equal(b, sboard):
            av.append(int(i))

    return av


#Starts game cycle with specified move input function, board viewing solution and the board object.
def gamestart(inpfun, view=False, b=None):
    global score, ssind
    if view:
        print('Game Start!')
    ssind = 0
    score = 0
    placenum(1, b)
    placenum(1, b)
    while True:
        contgame = controller(inpfun, b)
        if contgame != True:
            return (score, contgame)
        newnum(b)
        if view != False:
            view(b)

