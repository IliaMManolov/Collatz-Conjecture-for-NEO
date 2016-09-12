# WARNING: UNFINISHED
# Performance is currently cirtically low, both in terms of memory and speed.
# (i.e. DON'T try running it with more than a 1000 elements and memory per chunk
# of more than a MB)


'''
Description: A script that does the same as the numpy one, although with
database usage(wendelin.core and (in the future) NEO) instead of regular arrays
It works in the following way:
 - Create a database big enough to contain all elements
 - Create a buffer np.array that contains number-depth pairs
 - Climb up the tree in the same manner as the regular script before
 - Instead of simply adding the numbers to the database directly, I add them to
the buffer array
 - Once that array is filled, I sort it and then add it to the database
 - Also, instead of the simple check whether we've gone through a certain
number, this time I need to check the database and the buffer array


What works:
 - Small test cases


Issues:
 - Searching for numbers is PAINFULLY slow(requires a read off the hard drive
and going through the entire buffer, meaning that a bigger buffer reduces
performance)
 - Adding is also slow(needs to go through the part of the database containing
the smallest and the largest of the numbers and needs to sort the buffer)
 - probably others

To-do:
 - Swap the buffer array with something that has O(logN) search time, so that
searching isn't so slow. Using something that avoids duplicate elements is even
bretter.
 - other optimizations which I can't think of right now
'''

import numpy as np

from wendelin.bigarray.array_zodb import ZBigArray
from wendelin.lib.zodb import dbopen, dbclose
import transaction

def commitData(sourceArray, database, chunkSize):
    sourceArray = np.sort(sourceArray, order = 'number')
    sourceIndex = 0
    chunkEnd = database.size / chunkSize

    for chunkIndex in range(0, chunkEnd):
        currentView = database[chunkIndex * chunkSize : (chunkIndex + 1) * chunkSize]
        while (sourceIndex < sourceArray.size and sourceArray[sourceIndex]['number'] >= chunkIndex * chunkSize and sourceArray[sourceIndex]['number'] < (chunkIndex+1) * chunkSize):
            currentView[int(sourceArray[sourceIndex]['number']) - chunkIndex * chunkSize] = sourceArray[sourceIndex]['depth']
            sourceIndex += 1
        transaction.commit()
        if (sourceIndex == sourceArray.size):
            break
    transaction.commit()


def pushNumber(index, target, number, depth):
    target[index]['number'] = number
    target[index]['depth'] = depth

    index += 1

    if (index == target.size):
        commitData(target)
        index = 0
        return 0, True

    return index, False

def findInDatabase(depthData, toCommit, number):
    currentView = depthData[number:number+1]
    if (currentView[0] != 0):
        return True

    #print toCommit.size
    #print number
    #tmp = raw_input("hue")

    for index in range(0, toCommit.size):
        if (toCommit[index]['number'] == number):
            return True
    return False

def breadthFirstSearch(databaseSize, depthData, transactionSize, chunkSize):

    toCommit = np.zeros(transactionSize, np.dtype([('number', np.uint64), ('depth', np.uint32)]))
    commitIndex = 0

    # fill toCommit with pairs number-depth;
    # sort toCommit by numbers and go through the database step by step, filling
    # it with data from toCommit (complexity O(NlogN))

    currDepth = 1
    currTop = np.array([(1)], dtype = np.uint64)

    while (currTop.size != 0):
        newTop = np.array([], dtype = np.uint64)
        print currTop
        #tmp = raw_input("Press enter")
        for unsigned_number in currTop:
            number = int(unsigned_number)
            if (number<=databaseSize and findInDatabase(depthData, toCommit, number) == False):
                commitIndex, shouldCommit = pushNumber(commitIndex, toCommit, number, currDepth)
                if (shouldCommit):
                    commitData(toCommit, depthData, chunkSize)
                    toCommit = np.zeros(transactionSize, np.dtype([('number', np.uint64), ('depth', np.uint32)]))

                newTop = np.append(newTop, number*2)
                if (number > 1 and number%2 == 0 and (number-1)%3 == 0):
                    newTop = np.append(newTop, (number-1)/3)

        currTop = newTop
        currDepth += 1

    commitData(toCommit, depthData, chunkSize)


def main():
    root = dbopen('test.fs')

    databaseSize = input('Enter the highest number you want to get data from: ')

    ramSize = input('Enter the amount of RAM in MB to commit per transaction: ')
    transactionSize = ramSize * 1024 * 1024 / 12;

    chunkSize = input('Enter the number of elements to be processed at a time (divisors of the total size work best): ')

    root['depthData'] = depthData = ZBigArray((databaseSize, ), np.uint32)
    transaction.commit()

    breadthFirstSearch(databaseSize, depthData, transactionSize, chunkSize)

    transaction.commit()
    dbclose(root)



if __name__ == "__main__":
    main()
