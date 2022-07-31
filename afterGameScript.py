import os
from os.path import join

import shutil
# TODO: put in config:
from TestCaseFileObj import TestCaseFileObj
import Constants

# TODO:
# git diff 4e0a826761cb7d2bbaa8c50dae797383b886f0ec 3c332fcc7e33ad23db814a27d1074ab5d1700345 > C:\Users\Michael\Desktop\gitDiff.txt

#
# C:\Users\Michael\Desktop\gitDiff.txt
from TestOutputParser import sanityCheckNumbersAddUp, outputParser

# TODO: maybe the path before the folder name could be a config.


# TODO: Give the option of actually running the git diff command.

def doAfterGameAnalysis(gitDiffFilePath, outputPath):
    gitDiffDict = {}
    if gitDiffFilePath == '':
        pass
    else:
        gitDiffDict = goThruGitDiff(gitDiffFilePath)

    runTestCaseDict = outputParser(outputPath)

    print()
    print("Copying failed and important test cases to test folders:")

    # TODO: put folders in a list and refactor
    folderForBids = os.path.join(Constants.baseTestFolderPath, "newBidTestcases")

    folderForLeadFails = os.path.join(Constants.baseTestFolderPath, "newLeadFails")
    folderForFollowFails = os.path.join(Constants.baseTestFolderPath, "newFollowFails")

    if not os.path.exists(folderForBids):
        os.makedirs(folderForBids)

    if not os.path.exists(folderForLeadFails):
        os.makedirs(folderForLeadFails)

    if not os.path.exists(folderForFollowFails):
        os.makedirs(folderForFollowFails)
    # END TODO

    # TODO: be able to identify when test case is labelled with "(TODO: please test)"
    # TODO: put label in constants file
    folderForBonusCheck = os.path.join(Constants.baseTestFolderPath, "bonusChecks")

    countTestcasesMoved = 0

    for key in gitDiffDict:

        if key in runTestCaseDict.keys():

            testcase = runTestCaseDict[key]

            fromPath = os.path.join(Constants.baseTestFolderPath, gitDiffDict[key].getOrigFolderOfTestcase(),
                                    gitDiffDict[key].filename)

            testcaseMoved = 1

            if testcase.outcome == 0:

                if testcase.failType == 'lead':
                    shutil.copyfile(fromPath, os.path.join(folderForLeadFails, gitDiffDict[key].filename))
                elif testcase.failType == 'bid':
                    # TODO: delete this once you move all new bids to this folder
                    # Replace with pass
                    shutil.copyfile(fromPath, os.path.join(folderForBids, gitDiffDict[key].filename))
                else:
                    shutil.copyfile(fromPath, os.path.join(folderForFollowFails, gitDiffDict[key].filename))

            elif testcase.folder == "MichaelDebugMadeUp":
                shutil.copyfile(fromPath, os.path.join(folderForBonusCheck, gitDiffDict[key].filename))

            else:
                testcaseMoved = 0

            # TODO: check for (TODO: please test) label

            # TODO: be able to identify bids even though it's not a fail
            # TODO: count lead, second, third, fourth, and bid fails
            # TODO: do all the stats!

            countTestcasesMoved += testcaseMoved

        else:
            print(
                "Warning: (In afterGameScript) couldn't find " + key + "in run dictionary (but it was in the git "
                                                                       "diff)")

    # End of dictionary loop

    print("Done moving important new test cases, so monte could analyze them. "
          + str(countTestcasesMoved) + " test cases were moved.")


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

        #print(line)

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


if __name__ == '__main__':
    doAfterGameAnalysis("/Users/Michael/Desktop/gitDiff.txt", "/Users/Michael/Desktop/july24th-1.txt")
    # goThruGitDiff("/Users/Michael/Desktop/gitDiff.txt")
