from os import listdir
from os.path import join

from TestCaseFileObj import TestCaseFileObj


def makeFileObjectFromFile(folderPath, filename):
    nameOfPlayer = ''
    cards = ''

    file1 = open(join(folderPath, filename), 'r')

    previousLine = ''

    while True:

        # Get next line from file
        line = file1.readline()

        if line.startswith("Your name: "):
            nameOfPlayer = line.split(" ")[2].strip()
        elif previousLine.startswith("Cards in hand:"):
            cards = line.strip()

        previousLine = line
        # if line is empty
        # end of file is reached
        if not line:
            break

    file1.close()

    folder = folderPath.split("/")[-1]

    return TestCaseFileObj(filename, nameOfPlayer, cards, folder)


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


def goThruGitDiff(gitDiffFilepath):
    print()
    print("Going through TestCaseAndReplayData git diff to find new test cases:")

    file = open(join(gitDiffFilepath), 'r')
    testFileDict = {}

    previousLine = ''

    currentTestFileName = ''
    nameOfPlayer = ''
    cards = ''
    folder = ''

    count = 0

    while True:
        count += 1

        # Get next line from file
        line = file.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        if line.startswith("+"):
            line = line[1:]
        else:
            continue

        line = line.strip()

        # print(line)

        if line.startswith("++") and line.endswith(".txt"):

            if currentTestFileName != '':
                tmpFileObj = TestCaseFileObj(currentTestFileName, nameOfPlayer, cards, folder)

                if tmpFileObj.getKey() in testFileDict:
                    print("Warning: duplicate test case: " + tmpFileObj.getKey())
                    print("Removing prev test case from list")

                testFileDict[tmpFileObj.getKey()] = tmpFileObj

                # reinit vars just in case;
                nameOfPlayer = ''
                cards = ''
                # End reinit vars

            folder = line.split("/")[-2]
            currentTestFileName = line.split("/")[-1]

        elif line.startswith("Your name: "):
            nameOfPlayer = line.split(" ")[2].strip()

        elif previousLine.startswith("Cards in hand:"):
            cards = line.strip()

        previousLine = line

    file.close()

    lastTestcase = TestCaseFileObj(currentTestFileName, nameOfPlayer, cards, folder)

    if lastTestcase.getKey() in testFileDict:
        print("Warning: duplicate test case 2: " + lastTestcase.getKey())
        print("Removing prev test case from list 2")

    testFileDict[lastTestcase.getKey()] = lastTestcase

    print("Line count: " + str(count))
    print("numTestcases: " + str(len(testFileDict)))

    return testFileDict
