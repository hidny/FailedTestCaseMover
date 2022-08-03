import argparse

import Constants
from TestOutputParser import outputParser
import os
import shutil

import re


def changeFilenameToUndoCollisionIncrement(origFileName):
    fileNum = getNumberFromFilename(origFileName)

    if fileNum >= 10000:
        return "testcase" + str(fileNum % 10000) + ".txt"
    else:
        return origFileName


def getFileNameToUseToAvoidCollision(targetFolder, origFileName):
    if os.path.exists(os.path.join(targetFolder, origFileName)):
        fileNum = getNumberFromFilename(origFileName)

        InitialAddition = 100000
        increment = 10000
        i = 0
        while True:
            newFileNum = fileNum + InitialAddition + i * increment

            newFileName = "testcase" + str(newFileNum) + ".txt"

            if not os.path.exists(os.path.join(targetFolder, newFileName)):
                break
            else:
                i = i + 1

        return newFileName
    else:
        return origFileName


def getNumberFromFilename(filename):
    testCaseNumbers = re.findall(r'\d+', filename)

    if len(testCaseNumbers) != 1:
        print("Error: test case doesn't have 1 number")
        exit(0)

    else:
        return int(testCaseNumbers[0])


def main():
    parser = argparse.ArgumentParser(description=
                                     "Move labelled test cases to a new folder for further analysis.\n"
                                     "This needs an output file combined the relevant label.\n"
                                     "The label is not case sensitive and if no label is provided, the default label is todo")

    parser.add_argument("file", help="File name of the output file if on desktop. Otherwise, it's the full path")

    parser.add_argument("-f", "--folder", default="tmp",
                        help="Folder name of test folder to copy test cases to. The default is a folder named \"tmp\"")

    parser.add_argument("-l", "--label", default=Constants.DEFAULT_LABEL,
                        help="Label test case needs to have in order to copy it. Default label is \"" + Constants.DEFAULT_LABEL + "\"")

    args = parser.parse_args()

    if args.file.find("/") != -1 or args.file.find("\\") != -1:
        fullPathFile = args.file
    else:
        fullPathFile = os.path.join(Constants.DESKTOP_LOCATION, args.file)

    if args.folder.find('/') != -1 or args.folder.find('\\') != -1:
        print("Just put in the folder name without using the full path, or any path separators.")
        exit(1)
    elif args.folder in Constants.LIST_OF_FOLDERS:
        print("ERROR: the folder you used is part of the list of main folders where the test cases belong.")
        exit(1)

    outputTestcases = outputParser(fullPathFile, args.label)

    targetFolder = os.path.join(Constants.baseTestFolderPath, args.folder)

    print("Length of dict1: " + str(len(outputTestcases)))

    for key in outputTestcases:

        if outputTestcases.get(key).hasCustomLabel:
            print(key)

            destFileNameToUse = getFileNameToUseToAvoidCollision(targetFolder, outputTestcases[key].filename)

            shutil.copyfile(
                os.path.join(Constants.baseTestFolderPath, outputTestcases[key].getOrigFolderOfTestcase(),
                             outputTestcases[key].filename),
                os.path.join(targetFolder, destFileNameToUse))


if __name__ == '__main__':
    main()

# Example:
# python MLabelledTestcasesToFolder.py july22nd-1.txt -l "(FOURTH FAIL)"
