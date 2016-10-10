import sys
import numpy as np
import collatz_library as col

def main(arguments):

    #Getting command-line arguments
    startNumber = 1
    endNumber = 10000
    optimizationArrayMode = 0
    if (len(arguments)>=3):
        optimizationArrayMode = int(arguments[2])
    if (len(arguments)>=2):
        startNumber = int(arguments[0])
        endNumber = int(arguments[1])
    elif (len(arguments) == 1):
        endNumber = int(arguments[0])

    result = np.zeros((endNumber - startNumber + 1), dtype = np.uint32)


    #Using the library's bruteforce method to calculate the depths
    result = col.bruteforce(startNumber, endNumber+1, 1, optimizationArrayMode)


    #Printing the array
    col.printData(startNumber, result)


if (__name__ == "__main__"):
    main(sys.argv[1:])
