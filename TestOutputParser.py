# tODO: make this a helper function
from TestCaseFileObj import TestCaseFileObj


# TODO: maybe add option to get fail counts or test case list.
# TODO: compare fail counts to other output files so we could fill in the table


def outputParser(outputFilename):
    print()
    print("Reading Testcase Parser output:")
    print("Parser output filename: " + outputFilename)

    fileDict = {}

    file1 = open(outputFilename, 'r')

    # TODO: parse output file (The things that has all the test results)
    # And save it to dictionary...

    currentTestFileName = ''
    playerName = ''
    cardsInHand = ''
    # folder = ''
    outcome = 0
    failType = ''

    count = 0

    # TODO: maybe put all these vars in an object
    numTestcases = 0
    numPasses = 0
    numFails = 0
    numBidFails = 0
    numLeadFails = 0
    numSecondFails = 0
    numThirdFails = 0
    numFourthFails = 0
    # END TODO

    while True:
        count += 1

        # Get next line from file
        line = file1.readline()

        # if line is empty
        # end of file is reached
        if not line:
            if currentTestFileName != '':
                # TODO: copy/paste code is bad.
                tmpFileObj = TestCaseFileObj(currentTestFileName, playerName, cardsInHand, '', outcome, failType)
                # print("Key: " + tmpFileObj.getKey())

                if tmpFileObj.getKey() in fileDict:
                    print("Warning: duplicate test case: " + tmpFileObj.getKey())
                    print("Removing prev test case from list")

                fileDict[tmpFileObj.getKey()] = tmpFileObj
                # end todo: copy/paste code is bad.

            break

        line = line.strip()
        prevLine = line

        if line.startswith("#") == 0:
            if line.startswith("Testing"):

                sanityCheckNumbersAddUp(numTestcases,
                                        numPasses,
                                        numFails,
                                        numBidFails,
                                        numLeadFails,
                                        numSecondFails,
                                        numThirdFails,
                                        numFourthFails)

                if currentTestFileName != '':
                    tmpFileObj = TestCaseFileObj(currentTestFileName, playerName, cardsInHand, '', outcome, failType)
                    # print("Key: " + tmpFileObj.getKey())

                    if tmpFileObj.getKey() in fileDict:
                        print("Warning: duplicate test case: " + tmpFileObj.getKey())
                        print("Removing prev test case from list")

                    fileDict[tmpFileObj.getKey()] = tmpFileObj

                # reinit vars just in case;
                playerName = ''
                cardsInHand = ''
                # folder = ''
                outcome = 0
                failType = ''
                # End reinit vars

                currentTestFileName = line.split(" ")[-1]
                numTestcases = numTestcases + 1

            elif line.startswith("Your name: "):
                playerName = line.split(" ")[2].strip()

            elif prevLine.startswith("Cards left:"):
                cardsInHand = line.strip()

            elif line.find("(PASS)") != -1:
                numPasses = numPasses + 1
                outcome = 1
                # TODO: Maybe alt pass should have outcome = 2?

            elif line.find("(FAIL)") != -1:
                numFails = numFails + 1
                outcome = 0

            elif line.find("(BID FAIL)") != -1:
                numBidFails = numBidFails + 1
                failType = 'bid'

            elif line.find("(LEAD FAIL)") != -1:
                numLeadFails = numLeadFails + 1
                failType = 'lead'

            elif line.find("(SECOND FAIL)") != -1:
                numSecondFails = numSecondFails + 1
                failType = 'second'

            elif line.find("(THIRD FAIL)") != -1:
                numThirdFails = numThirdFails + 1
                failType = 'third'

            elif line.find("(FOURTH FAIL)") != -1:
                numFourthFails = numFourthFails + 1
                failType = 'fourth'

            # TODO: search for other labels...

        # print("Line{}: {}".format(count, line.strip()))

    file1.close()

    print("Line count: " + str(count))
    print("numTestcases: " + str(numTestcases))
    print("numPasses: " + str(numPasses))
    print("numFails: " + str(numFails))
    print("numBidFails: " + str(numBidFails))
    print("numLeadFails: " + str(numLeadFails))
    print("numSecondFails: " + str(numSecondFails))
    print("numThirdFails: " + str(numThirdFails))
    print("numFourthFails: " + str(numFourthFails))

    return fileDict


def sanityCheckNumbersAddUp(numTestcases, numPasses, numFails, numBidFails, numLeadFails, numSecondFails, numThirdFails,
                            numFourthFails):
    if numTestcases != numPasses + numFails:
        print("WARNING: test cases don't add up 1")

    if numFails != numBidFails + numLeadFails + numSecondFails + numThirdFails + numFourthFails:
        print("WARNING: test cases don't add up 2")


if __name__ == '__main__':
    outputParser("/Users/Michael/Desktop/july24th-1.txt")

'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", help="Test case output filename",
                    type=str)

args = parser.parse_args()

if args.filename:
    print(args.filename)

    outputParser(args.filename)

'''
