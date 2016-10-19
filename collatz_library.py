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
def bruteforce(startNumber, endNumber, dataFirstNumber = -1, optimizationArrayMode = 0, calculatedArray = np.zeros(1, )):


    #Setting up the optimization array
    optimizationArray = 0
    if (optimizationArrayMode == 0):
        optimizationArray = np.array([])        #0th case - no optimization
    if (optimizationArrayMode == 1):
        optimizationArray = np.zeros((1000), dtype = np.uint32)    #1st case - empty with 1000 elements
    elif (optimizationArrayMode == 2):
        optimizationArray = np.zeros((endNumber - startNumber), dtype = np.uint32)   #2nd case - empty with as many elements as the regular array
    elif (optimizationArrayMode == 3):
        optimizationArray = bruteforce(1, 1000)             #3rd case - filled with answers up to 1000
    else:
        optimizationArray = bruteforce(1, optimizationArrayMode) #4th case - filled with answers up to the argument

    results = np.zeros((endNumber - startNumber + 1), dtype = np.uint32)
    for number in range(startNumber, endNumber):
        if (calculatedArray.size!=1 and calculatedArray[number - startNumber] != 0):
            results[number - startNumber] = calculatedArray[number - startNumber]
        else:
            tmpNumber = number
            steps = 0

            while (tmpNumber != 1 and exists(tmpNumber, dataFirstNumber, optimizationArray) == -1):
                if (tmpNumber % 2 == 0):
                    tmpNumber/=2
                else:
                    tmpNumber = tmpNumber * 3 + 1
                steps+=1

            if (tmpNumber == 1):
                results[number - startNumber] = steps
            else:
                results[number - startNumber] = exists(tmpNumber, dataFirstNumber, optimizationArray) + steps

            if (dataFirstNumber != -1 and number >= dataFirstNumber and number < dataFirstNumber + optimizationArray.size):
                optimizationArray[number - dataFirstNumber] = results[number-startNumber]

    return results
