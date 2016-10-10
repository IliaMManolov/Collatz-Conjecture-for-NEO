import numpy as np
import sys
import collatz_library as col

from wendelin.bigarray.array_zodb import ZBigArray
from wendelin.lib.zodb import dbopen, dbclose
import transaction



def main(arguments):

    #Getting command-line arguments
    startNumber = 1
    endNumber = 10000
    optimizationArrayMode = 0
    chunkSize = 100000

    if (len(arguments)>=5):
        databaseLocation = arguments[4]
    if (len(arguments)>=4):
        chunkSize = arguments[3]
    if (len(arguments)>=3):
        optimizationArrayMode = int(arguments[2])
    if (len(arguments)>=2):
        startNumber = int(arguments[0])
        endNumber = int(arguments[1])
    elif (len(arguments) == 1 and arguments[0] == 'help'):
        print 'This script calculates a list of numbers\' Collatz Conjecture Depth'
        print 'Usage:'
        print '   help - brings out this screen'
        print '   *no parameters* - calculates the first 10000 numbers and writes them in a file named collatz.fs'
        print '   /startNumber/ /endNumber/ /optimizationMode/ /chunkSize/ /databaseLocation/ - for custom calculations'

    #opening the NEO database
    root = dbopen('neo://neo-iliya-comp-2592@[2001:67c:1254:2b::347e]:2051')


    root['collatz'] = target = ZBigArray((endNumber - startNumber + 1, ), np.uint32)
    transaction.commit()


    sectorCount = (endNumber - startNumber) /chunkSize
    for sector in range(0, sectorCount):
        #Using the library's bruteforce method to calculate the depths
        tmpStorage = target[sector * chunkSize + startNumber:(sector+1) * chunkSize + startNumber]
        tmpResults = col.bruteforce(sector * chunkSize + startNumber, (sector+1) * chunkSize + startNumber, 1, optimizationArrayMode)

        tmpStorage[:] = tmpResults[:]

        transaction.commit()
        print 'Calculated chunk %d of %d' %(sector, sectorCount)

    db.close()





if (__name__ == "__main__"):
    main(sys.argv[1:])
