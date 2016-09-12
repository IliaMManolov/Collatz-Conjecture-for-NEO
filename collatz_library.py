import numpy as np

# Utility function that checks if we have already calculated data for a given number
def exists(number, dataFirstNumber, dataArray):
    if (dataFirstNumber == -1 or number < dataFirstNumber or number >= dataFirstNumber + dataArray.size):
        return -1

    if (dataArray[number - dataFirstNumber] == 0):
        return -1

    return dataArray[number - dataFirstNumber]

def printData(startNumber, array):
    for number in range(0, array.size-1):
        print '%d is %d deep' %((number + startNumber), array[number])

# Regular Bruteforce function for calculating the conjecture - goes through all numbers specified and
# tries to optimize by checking a given precalculated array
def bruteforce(startNumber, endNumber, dataFirstNumber = -1, dataArray = np.array([])):

    results = np.zeros((endNumber - startNumber + 1), dtype = np.uint32)
    for number in range(startNumber, endNumber):
        tmpNumber = number
        steps = 0

        while (tmpNumber != 1 and exists(tmpNumber, dataFirstNumber, dataArray) == -1):
            if (tmpNumber % 2 == 0):
                tmpNumber/=2
            else:
                tmpNumber = tmpNumber * 3 + 1
            steps+=1

        if (tmpNumber == 1):
            results[number - startNumber] = steps
        else:
            results[number - startNumber] = exists(tmpNumber, dataFirstNumber, dataArray) + steps

        if (dataFirstNumber != -1 and number >= dataFirstNumber and number < dataFirstNumber + dataArray.size):
            dataArray[number - dataFirstNumber] = results[number-startNumber]

    return results
