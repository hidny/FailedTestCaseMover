from os.path import join

import Constants
from TestCaseFileObj import TestCaseFileObj
from TestCaseOutcomeCounters import TestCaseOutcomeCounters


# TODO: at least try to eliminate copy/paste code:

def makeFileObjectFromFile(folderPath, filename, customLabel=''):
    nameOfPlayer = ''
    cards = ''
    prevBidHistoryLine = 0
    isBid = 1
    hasTODOLabel = 0
    hasCustomLabel = 0

    file1 = open(join(folderPath, filename), 'r')

    previousLine = ''

    count = 0

    while True:

        count = count + 1
        # Get next line from file
        line = file1.readline()

        if line.startswith("Your name: "):
            nameOfPlayer = line.split(" ")[2].strip()
        elif previousLine.startswith("Cards in hand:"):
            cards = line.strip()
        elif line.startswith("Bid history:"):
            prevBidHistoryLine = count
        elif line.find(" bid ") != -1 and count - prevBidHistoryLine == Constants.NUM_PLAYERS:
            isBid = 0

        if line.lower().find("todo") != -1:
            hasTODOLabel = 1

        if customLabel != '' and line.lower().find(customLabel.lower()) != -1:
            hasCustomLabel = 1

        previousLine = line
        # if line is empty
        # end of file is reached
        if not line:
            break

    file1.close()

    folder = folderPath.split("/")[-1]

    return TestCaseFileObj(filename, nameOfPlayer, cards, isBid, hasTODOLabel, hasCustomLabel, folder)


def outputParser(outputFilename, customLabel=''):
    print()
    print("Reading Testcase Parser output:")
    print("Parser output filename: " + outputFilename)

    fileDict = {}

    file1 = open(outputFilename, 'r')

    currentTestFileName = ''
    playerName = ''
    cardsInHand = ''
    prevCardsDealtLine = 0
    isBid = 1
    hasTODOLabel = 0
    hasCustomLabel = 0
    # folder = ''
    outcome = 0
    failType = ''

    count = 0

    counter = TestCaseOutcomeCounters()

    while True:
        count += 1

        # Get next line from file
        line = file1.readline()

        # if line is empty
        # end of file is reached
        if not line:
            if currentTestFileName != '':

                counter.sanityCheckNumbersAddUp()

                # TODO: copy/paste code is bad.
                tmpFileObj = TestCaseFileObj(currentTestFileName, playerName, cardsInHand, isBid, hasTODOLabel,
                                             hasCustomLabel,
                                             '', outcome, failType)
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

                counter.sanityCheckNumbersAddUp()

                if currentTestFileName != '':
                    tmpFileObj = TestCaseFileObj(currentTestFileName, playerName, cardsInHand, isBid, hasTODOLabel,
                                                 hasCustomLabel,
                                                 '', outcome, failType)
                    # print("Key: " + tmpFileObj.getKey())

                    if tmpFileObj.getKey() in fileDict:
                        print("Warning: duplicate test case: " + tmpFileObj.getKey())
                        print("Removing prev test case from list")

                    fileDict[tmpFileObj.getKey()] = tmpFileObj

                # reinit vars just in case;
                playerName = ''
                cardsInHand = ''
                isBid = 1
                hasTODOLabel = 0
                hasCustomLabel = 0
                # folder = ''
                outcome = 0
                failType = ''
                # End reinit vars

                currentTestFileName = line.split(" ")[-1]

                counter.incrementNumTestcases()

            elif line.startswith("Your name: "):
                playerName = line.split(" ")[2].strip()

            elif prevLine.startswith("Cards left:"):
                cardsInHand = line.strip()

            elif line.find("(PASS)") != -1:
                counter.incrementNumPasses()
                outcome = 1
                # TODO: Maybe alt pass should have outcome = 2?

            elif line.find("(FAIL)") != -1:
                counter.incrementNumFails()
                outcome = 0

            elif line.find("(BID FAIL)") != -1:
                counter.incrementNumBidFails()
                failType = 'bid'

            elif line.find("(LEAD FAIL)") != -1:
                counter.incrementNumLeadFails()
                failType = 'lead'

            elif line.find("(SECOND FAIL)") != -1:
                counter.incrementNumSecondFails()
                failType = 'second'

            elif line.find("(THIRD FAIL)") != -1:
                counter.incrementNumThirdFails()
                failType = 'third'

            elif line.find("(FOURTH FAIL)") != -1:
                counter.incrementNumFourthFails()
                failType = 'fourth'

            elif line.startswith("Cards dealt:"):
                prevCardsDealtLine = count

            elif not line.startswith("AI handle") \
                    and line.find(" bid ") != -1 \
                    and count - prevCardsDealtLine == 3 + Constants.NUM_PLAYERS:
                isBid = 0

        # General checks:
        if line.lower().find("todo") != -1:
            hasTODOLabel = 1
        if customLabel != '' and line.lower().find(customLabel.lower()) != -1:
            hasCustomLabel = 1

        # print("Line{}: {}".format(count, line.strip()))

    file1.close()

    print("Line count: " + str(count))
    counter.printCounterSums()

    return fileDict


def goThroughGitDiff(gitDiffFilepath, customLabel=''):
    print()
    print("Going through TestCaseAndReplayData git diff to find new test cases:")

    file = open(join(gitDiffFilepath), 'r')
    testFileDict = {}

    previousLine = ''

    currentTestFileName = ''
    nameOfPlayer = ''
    cards = ''
    prevBidHistoryLine = -1000
    isBid = 1
    hasTODOLabel = 0
    hasCustomLabel = 0
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
                tmpFileObj = TestCaseFileObj(currentTestFileName, nameOfPlayer, cards, isBid, hasTODOLabel,
                                             hasCustomLabel, folder)

                if tmpFileObj.getKey() in testFileDict:
                    print("Warning: duplicate test case: " + tmpFileObj.getKey())
                    print("Removing prev test case from list")

                testFileDict[tmpFileObj.getKey()] = tmpFileObj

                # reinit vars just in case;
                nameOfPlayer = ''
                cards = ''
                isBid = 1
                hasTODOLabel = 0
                hasCustomLabel = 0
                # End reinit vars

            folder = line.split("/")[-2]
            currentTestFileName = line.split("/")[-1]

        elif line.startswith("Your name: "):
            nameOfPlayer = line.split(" ")[2].strip()

        elif previousLine.startswith("Cards in hand:"):
            cards = line.strip()

        elif line.startswith("Bid history:"):
            prevBidHistoryLine = count

        elif line.find(" bid ") != -1 and count - prevBidHistoryLine == Constants.NUM_PLAYERS:
            isBid = 0

        if line.lower().find("todo") != -1:
            hasTODOLabel = 1

        if customLabel != '' and line.lower().find(customLabel.lower()) != -1:
            hasCustomLabel = 1

        previousLine = line

    file.close()

    lastTestcase = TestCaseFileObj(currentTestFileName, nameOfPlayer, cards, isBid, hasTODOLabel, hasCustomLabel,
                                   folder)

    if lastTestcase.getKey() in testFileDict:
        print("Warning: duplicate test case 2: " + lastTestcase.getKey())
        print("Removing prev test case from list 2")

    testFileDict[lastTestcase.getKey()] = lastTestcase

    print("Line count: " + str(count))
    print("numTestcases: " + str(len(testFileDict)))

    return testFileDict
