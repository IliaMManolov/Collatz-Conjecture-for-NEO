'''
Description: This source file is a simple, partial, but fast computation of the
Collatz conjecture(or at least the depth of its elements). It utilizes a BFS
(Breadth-first search) to climb up the tree of the conjecture and on each
step it tags the element's depth.
Unlike other solutions this one is partial in that whenever a number
becomes greater than storage, it's ignored and all of its children as well.
The advantage of doing this is that, in terms of computation, we can guarantee
sub-O(N) time and memory of N elements. The disadvantage is that it calculates
only some elements, thus large chunks of the result are undefined (or just 0).
We, however, can use this as our advantage when we later add compatibility
with NEO to test its compression.

'''

import numpy as np


# The BFS algorithm - nothing too fancy here
def breadthFirstSearch():
    global depthArray
    global arraySize

    currDepth = 1
    currTop = np.array([(1)], dtype = np.uint64)

    while (currTop.size != 0):
        newTop = np.array([], dtype = np.uint64)
        for unsigned_number in currTop:
            number = int(unsigned_number)
            if (number<=arraySize and depthArray[number] == 0):
                depthArray[number] = currDepth
                newTop = np.append(newTop, number * 2)
                if (number > 1 and number%2 == 0 and (number - 1)%3 == 0):
                    newTop = np.append(newTop, (number-1)/3)

        currTop = newTop

        currDepth = currDepth + 1

# A printing function to show off the depths
def printDepths():
    global depthArray
    for i in range(1, depthArray.size):
        print "%d is %d deep" % (i, depthArray[i])




arraySize = input('Enter the size of the depth array: ')

depthArray = np.zeros((arraySize+1), dtype = np.uint64)

breadthFirstSearch()
printDepths()
