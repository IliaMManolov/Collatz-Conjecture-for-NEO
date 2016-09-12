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

    #Setting up the optimization array
    optimizationArray = 0
    if (optimizationArrayMode == 1):
        optimizationArray = np.zeros((1000), dtype = np.uint32)    #1st case - empty with 1000 elements
    elif (optimizationArrayMode == 2):
        optimizationArray = np.zeros((endNumber - startNumber), dtype = np.uint32)   #2nd case - empty with as many elements as the regular array
    elif (optimizationArrayMode == 3):
        optimizationArray = col.bruteforce(1, 1000)             #3rd case - filled with answers up to 1000
    else:
        optimizationArray = np.array([])        #fallback case - empty(no optimization)

    #Using the library's bruteforce method to calculate the depths
    result = col.bruteforce(startNumber, endNumber+1, 1, optimizationArray)


    #Printing the array
    col.printData(startNumber, result)


if (__name__ == "__main__"):
    main(sys.argv[1:])
