import subprocess
import os
import Constants
from UselessTestCaseCrawler import makeFileObjectFromFile
import argparse


def getPrevFileName(numPrev, prevTestType, numCards=0):
    curTestFolder = os.path.join(Constants.baseTestFolderPath, Constants.curTestFolderBeingAddedTo)

    files = [f for f in os.listdir(curTestFolder) if os.path.isfile(os.path.join(curTestFolder, f))]

    files.sort()

    if numPrev >= len(files):
        print("ERROR: the number of previous files input is too big for the current folder"
              " (" + Constants.curTestFolderBeingAddedTo + ")")
        exit(1)

    if prevTestType == 0:
        print("File to open: " + files[-numPrev])

        return os.path.join(curTestFolder, files[-numPrev])

    elif prevTestType == 1:
        numFound = 0

        for file in reversed(files):
            if len(makeFileObjectFromFile(curTestFolder, file).cardsInHand.strip().split(" ")) == numCards \
                    and makeFileObjectFromFile(curTestFolder, file).isBid == 0:

                numFound = numFound + 1

                if numFound == numPrev:
                    print("File to open: " + file)
                    return os.path.join(curTestFolder, file)

    elif prevTestType == 2:
        numFound = 0

        for file in reversed(files):
            if makeFileObjectFromFile(curTestFolder, file).isBid == 1:

                numFound = numFound + 1

                if numFound == numPrev:
                    print("File to open: " + file)
                    return os.path.join(curTestFolder, file)

    print("ERROR: the number of previous files input is too big for the current folder"
          " (" + Constants.curTestFolderBeingAddedTo + ")")
    print("Hint: Maybe try removing the filter you used.")
    exit(1)


def findRelevantFileBasedOnArgs(args):
    # Default is to just go back to the last one:
    numPrev = 1
    numCards = 0

    prevTestType = 0
    if args.num:
        numPrev = args.num
        if numPrev < 0:
            print("ERROR: a negative number for nth last test case is not acceptable")
            exit(1)
        prevTestType = 0

    if args.card:
        prevTestType = 1
        numCards = args.card

    elif args.bid:
        prevTestType = 2

    return getPrevFileName(numPrev, prevTestType, numCards)


def main():
    parser = argparse.ArgumentParser(description='Open previous testcase, so you can quickly edit it.')

    listCardNumAvailable = []
    for i in range(2, Constants.MAX_CARDS_IN_A_HAND + 1):
        listCardNumAvailable.append(i)

    parser.add_argument("-n", "--num", help="Get the nth last test case", type=int)

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-c", "--card", help="Filter for non-bid test cases with a specific number of cards", type=int,
                       choices=listCardNumAvailable)
    group.add_argument("-b", "--bid", help="Filter for bid test cases", action="store_true")

    args = parser.parse_args()

    fileToOpen = findRelevantFileBasedOnArgs(args)
    subprocess.call([Constants.notepadPPLocation, fileToOpen])


if __name__ == '__main__':
    main()
