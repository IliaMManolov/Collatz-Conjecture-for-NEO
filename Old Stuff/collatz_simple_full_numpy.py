# WARNING: This script doesn't work properly due to high memory usage when going
# down the tree.

'''
This source file is a simple and full computation of the Collatz conjecture,
which uses the same algorithm as the previous one. The difference here is
that instead of ignoring elements outside the scope of our array, we keep
them in the tree just in case at some moment we reach an undiscovered element
that we haven't reached yet. This algorithm isn't fast, it's actually really
slow with big numbers, so I've added a variable that tells at what point the
program should stop(some percent of the total number). Otherwise, if given
enough time and set to 100, the program will find the depth of all elements
inside the array.

'''

import numpy as np


#The BFS algorithm - nearly the same as the original
def breadthFirstSearch():
    global depthArray
    global arraySize
    global fillPercent

    currDepth = 1
    currFill = 0
    arrayCapacity = (int)((fillPercent/100.0) * arraySize)
    print arrayCapacity

    currTop = np.array([(1)], dtype = np.uint64)

    while (currFill < arrayCapacity):
        print 'currTop:'
        print currTop
        newTop = np.array([], dtype = np.uint64)
        for unsigned_number in currTop:
            number = int(unsigned_number)
            if (number<=arraySize and depthArray[number] == 0):
                depthArray[number] = currDepth
                currFill+=1
            if (number*2>arraySize or depthArray[number*2] == 0):
                newTop = np.append(newTop, number * 2)
            if (number > 1 and (number - 1)%3 == 0):
                x = (number-1)/3
                if (x>arraySize or depthArray[x] == 0):
                    newTop = np.append(newTop, x)

        currTop = newTop

        currDepth += 1

# A printing function to show off the depths
def printDepths():
    global depthArray
    for i in range(1, depthArray.size):
        print "%d is %d deep" % (i, depthArray[i])




arraySize = input('Enter the size of the depth array: ')
fillPercent = input('Enter what percent of the array you want filled: ')

depthArray = np.zeros((arraySize+1), dtype = np.uint64)

breadthFirstSearch()
printDepths()
