import numpy as np

from wendelin.bigarray.array_zodb import ZBigArray
from wendelin.lib.zodb import dbopen, dbclose
import transaction


def checkCalculated(number, depthBuffer, startNumber, endNumber):
    if (number == 0):
        return 0
    if (number == 1):
        return 1
    if (number < startNumber or number >= endNumber):
        return -1

    index = number - startNumber
    if (depthBuffer[index] == 0):
        return -1

    return depthBuffer[index]


def Bruteforce(databaseSize, depthData, transactionSize):
    transactionCount = databaseSize / transactionSize + (databaseSize % transactionSize != 0)
    print transactionCount

    for transactionIndex in range(0, transactionCount):
        transactionStart = transactionIndex * transactionSize
        transactionEnd = transactionStart + min(transactionSize, databaseSize - transactionStart)
        depthBuffer = np.zeros(transactionEnd - transactionStart, np.uint32)

        for currentNumber in range (transactionStart, transactionEnd):
            result = 0
            tmpNumber = currentNumber
            while (checkCalculated(tmpNumber, depthBuffer, transactionStart, transactionEnd) == -1):
                if (tmpNumber % 2 == 0):
                    tmpNumber /= 2
                else:
                    tmpNumber = tmpNumber * 3 + 1
                result += 1
            result += checkCalculated(tmpNumber, depthBuffer, transactionStart, transactionEnd)
            depthBuffer[currentNumber - transactionStart] = result

            #print '%d : %d' %(currentNumber, result)

        currentView = depthData[transactionStart: transactionEnd]
        for i in range(0, depthBuffer.size):
            currentView[i] = depthBuffer[i]

        transaction.commit()
        print '%d percent done' % ((transactionIndex + 1) * (100.0/transactionCount))

    transaction.commit()





def main():
    root = dbopen('test2.fs')

    databaseSize = input('Enter the highest number you want to get data from: ')

    ramSize = input('Enter the amount of RAM in MB to commit per transaction: ')
    transactionSize = ramSize * 1024 * 1024 / 8;

    root['depthData'] = depthData = ZBigArray((databaseSize, ), np.uint32)
    transaction.commit()

    Bruteforce(databaseSize, depthData, transactionSize)

    transaction.commit()
    dbclose(root)



if __name__ == "__main__":
    main()
