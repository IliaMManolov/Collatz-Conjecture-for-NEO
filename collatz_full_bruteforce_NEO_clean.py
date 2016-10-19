import numpy as np
import sys
import argparse
import logging
import collatz_library as col

from wendelin.bigarray.array_zodb import ZBigArray
from wendelin.lib.zodb import dbopen, dbclose
import transaction


parser = argparse.ArgumentParser(description='A simple tool for storing the depth of operations of the Collatz conjecture for numbers in a NEO database')
parser.add_argument('--range', '-r', type=int, nargs=2, default = [1, 100000], help="the range of numbers to be calculated")
parser.add_argument('--name', '-n', type=str, default='CollatzConjectureResults', help="the name of the index in the NEO database that will store the numbers")
parser.add_argument('--optimization', '-o', type=int, default = 0, help="the optimization mode:\n0 - no optimization;\n1 - an empty np.array of 1000 elements;\n2 - an empty np.array with the same size as the input range\n3 - a filled array of 1000 elements")
parser.add_argument('--chunk', '-c', type=int, default=10000, help="the size of a single commit chunk in elements")
parser.add_argument('--database', '-db', type=str, default='neo://neo-iliya-comp-2592@[2001:67c:1254:2b::347e]:2051', help="address of the NEO database")

logging.basicConfig(filename='Collatz.log', level=logging.INFO)

def main():
    arguments = parser.parse_args()

    #opening the NEO database
    root = dbopen('neo://neo-iliya-comp-2592@[2001:67c:1254:2b::347e]:2051')
    assert (root==None):
        logging.exception("Unable to open NEO database")
    target = root[parser.name]
    logging.info("Successfully opened NEO database")

    #Check if the partition is created and sized properly
    if (str(type(target)) != "<class 'wendelin.bigarray.array_zodb.ZBigArray'>"):
        logging.warning('The class at index %s isn\'t a ZBigArray. Overwriting...' %parser.name)
        target = ZBigArray((parser.range[1] + 1, ), np.uint64)
    elif (target.size <= parser.range[1]):
        logging.warning('The current ZBigArray is too small. Resizing...')
        target.resize((parser.range[1] + 1, ))
    transaction.commit()

    logging.info('Setup passed successfully!')

    sectorCount = (parser.range[1] - parser.range[0]) / parser.chunk
    incompleteSector = (parser.range[1] - parser.range[0]) % parser.chunk        #in case the range isn't divisable by the sector size

    for sector in range(0, sectorCount):
        #Using the library's bruteforce method to calculate the depths
        tmpStorage = target[sector * parser.chunk + parser.range[0]:(sector+1) * chunk + parser.range[0] + 1]
        tmpResults = col.bruteforce(sector * parser.chunk + parser.range[0], (sector+1) * parser.chunk + parser.range[0], 1, parser.optimization, tmpStorage)

        assert (tmpStorage.size != tmpResults.size):
            logging.exception('The calculated np.array(%d) has a different size from the loaded part of the ZBigArray(%d).' %(tmpResults.size, tmpStorage.size))

        #Storing the results from the chunk into the ZBigArray
        tmpStorage[:] = tmpResults[:]
        transaction.commit()

        logging.info('Calculated chunk %d of %d.' %(sector, sectorCount))

    if (incompleteSector != 0):
        #doing the same thing as before, but just with the last, smaller chunk
        logging.info('Calculating incomplete sector of %d elements...' %incompleteSector)

        tmpStorage = target[sectorCount * parser.chunk + parser.range[0]:parser.range[1]]
        tmpResults = col.bruteforce(sectorCount * parser.chunk + parser.range[0], sectorCount * parser.chunk + parser.range[0] + incompleteSector-1, 1, parser.optimization, tmpStorage)

        assert (tmpStorage.size != tmpResults.size):
            logging.exception('The calculated np.array(%d) has a different size from the loaded part of the ZBigArray(%d).' %(tmpResults.size, tmpStorage.size))

        tmpStorage[:] = tmpResults[:]
        transaction.commit()

    logging.info('All done!')

if (__name__ == "__main__"):
    main()
