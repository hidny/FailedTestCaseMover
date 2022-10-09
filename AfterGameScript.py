import os

import shutil
import Constants
import subprocess
import argparse


from TestCaseOutcomeCounters import TestCaseOutcomeCounters
from TestcaseParsers import goThroughGitDiff, outputParser


def doAfterGameAnalysis(gitDiffFilePath, outputPath):
    gitDiffDict = {}
    if gitDiffFilePath == '':
        pass
    else:
        gitDiffDict = goThroughGitDiff(gitDiffFilePath)

    runTestCaseDict = outputParser(outputPath)

    print()
    print("Copying important new test cases to test folders\n"
          "(this includes newly failed tests, all bid test cases, and maybe some bonus tests):")

    # TODO: make a function and clean this up
    folderForBids = os.path.join(Constants.baseTestFolderPath, "newBidTestcases")

    folderForLeadFails = os.path.join(Constants.baseTestFolderPath, "newLeadFails")
    folderForFollowFails = os.path.join(Constants.baseTestFolderPath, "newFollowFails")

    folderForBonusCheck = os.path.join(Constants.baseTestFolderPath, "newBonusChecks")

    if not os.path.exists(folderForBids):
        os.makedirs(folderForBids)

    if not os.path.exists(folderForLeadFails):
        os.makedirs(folderForLeadFails)

    if not os.path.exists(folderForFollowFails):
        os.makedirs(folderForFollowFails)

    if not os.path.exists(folderForBonusCheck):
        os.makedirs(folderForBonusCheck)
    # END TODO

    countTestcasesMoved = 0

    # Move test cases around:

    for key in gitDiffDict:

        if key in runTestCaseDict.keys():

            testcase = runTestCaseDict[key]

            fromPath = os.path.join(Constants.baseTestFolderPath, gitDiffDict[key].getOrigFolderOfTestcase(),
                                    gitDiffDict[key].filename)

            testcaseMoved = 1
            if testcase.isBid == 1:
                shutil.copyfile(fromPath, os.path.join(folderForBids, gitDiffDict[key].filename))

            elif testcase.outcome == 0:

                if testcase.failType == 'lead':
                    shutil.copyfile(fromPath, os.path.join(folderForLeadFails, gitDiffDict[key].filename))
                elif testcase.failType == 'bid':
                    # This case shouldn't happen...
                    pass
                else:
                    shutil.copyfile(fromPath, os.path.join(folderForFollowFails, gitDiffDict[key].filename))

            elif testcase.folder == "MichaelDebugMadeUp":
                shutil.copyfile(fromPath, os.path.join(folderForBonusCheck, gitDiffDict[key].filename))

            elif testcase.hasTODOLabel == 1:
                shutil.copyfile(fromPath, os.path.join(folderForBonusCheck, gitDiffDict[key].filename))

            else:
                testcaseMoved = 0

            countTestcasesMoved += testcaseMoved

        else:
            print()
            print("******************")
            print(
                "Warning: (In afterGameScript) couldn't find key (" + key +
                ") in run dictionary (but it was in the git diff)")
            print("******************")
            print()

    # End of dictionary loop

    print("Done moving important new test cases, so monte could analyze them. ")
    print(str(countTestcasesMoved) + " test cases were moved.")

    # Do failure count:
    counterBefore = TestCaseOutcomeCounters()

    counterAfter = TestCaseOutcomeCounters()

    counterDuring = TestCaseOutcomeCounters()

    for key in runTestCaseDict:

        counterAfter.incrementCounterBasedOnTestcaseObj(runTestCaseDict[key])

        if key in gitDiffDict.keys():
            counterDuring.incrementCounterBasedOnTestcaseObj(runTestCaseDict[key])
        else:
            counterBefore.incrementCounterBasedOnTestcaseObj(runTestCaseDict[key])

    counterBefore.printSummaryPercentages("Before")

    counterAfter.printSummaryPercentages("After")

    counterDuring.printSummaryPercentages("During")

    # print("Debug:")
    # counterBefore.printCounterSums()
    # counterAfter.printCounterSums()
    # print("Sums to use:")
    # counterDuring.printCounterSums()

    print("Notebook sums:")
    counterBefore.printNotebookSums()
    counterAfter.printNotebookSums()

    # This matches the notebook summary I've been using:
    print("Sums to use:")
    counterDuring.printNotebookSums()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Do the after-game organizations rituals automatically')

    parser.add_argument("filename", help="File name if on desktop, or full path")

    parser.add_argument("-c", "--commit",
                        help="Commit id that we want to compare current testcases to. Defaults to last commit")

    args = parser.parse_args()

    if args.filename.find("/") != -1 or args.filename.find("\\") != -1:
        fullPathRun = args.filename
    else:
        fullPathRun = os.path.join(Constants.DESKTOP_LOCATION, args.filename)

    commitId = ''
    if args.commit:
        commitId = args.commit

    pr = subprocess.Popen("git add *txt", cwd=Constants.gitRepoFolderPath, shell=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

    (out, error) = pr.communicate()
    print("Error out1: " + str(error))

    if commitId == '':

        pr = subprocess.Popen("git log --format=%H -n 1", cwd=Constants.gitRepoFolderPath, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

        (out, error) = pr.communicate()
        commitId = str(out).replace("\\n", "").split("'")[1]

        print("Error out2: " + str(error))
        print("Commit ID: " + commitId)

    pr = subprocess.Popen("git diff " + commitId, cwd=Constants.gitRepoFolderPath, shell=True,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    (out, error) = pr.communicate()
    print("Error out3: " + str(error))

    out2 = str(out).replace("\\n", "\n")
    # print("out : " + out2)

    with open('tmpDiff.txt', 'w') as f:
        f.write(out2)

    # For testing:
    # doAfterGameAnalysis("/Users/Michael/Desktop/gitDiff.txt", "/Users/Michael/Desktop/july24th-1.txt")
    # goThruGitDiff("/Users/Michael/Desktop/gitDiff.txt")

    # python AfterGameScript.py july24th-1.txt -c 844ea0c57c112bc827a780a8a108b9868589c7aa
    # python AfterGameScript.py july24th-1.txt -c 4e0a826761cb7d2bbaa8c50dae797383b886f0ec

    doAfterGameAnalysis("tmpDiff.txt", fullPathRun)
