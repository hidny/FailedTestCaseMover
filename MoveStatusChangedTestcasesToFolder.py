import argparse

import Constants
from TestOutputParser import outputParser
import os
import shutil


def main():

    parser = argparse.ArgumentParser(description='Move Test cases with a status change between output files to a new folder for further analysis')

    parser.add_argument("file1", help="File name of the first file if on desktop. Otherwise, it's the full path")
    parser.add_argument("file2", help="File name of the second file if on desktop. Otherwise, it's the full path")

    parser.add_argument("-f", "--folder", default="tmp",
                        help="Folder name of test folder to copy test cases to. The default is a folder named \"tmp\"")

    args = parser.parse_args()

    if args.file1.find("/") != -1 or args.file1.find("\\") != -1:
        fullPathFile1 = args.file1
    else:
        fullPathFile1 = os.path.join(Constants.DESKTOP_LOCATION, args.file1)

    if args.file2.find("/") != -1 or args.file2.find("\\") != -1:
        fullPathFile2 = args.file2
    else:
        fullPathFile2 = os.path.join(Constants.DESKTOP_LOCATION, args.file2)

    if args.folder.find('/') != -1 or args.folder.find('\\') != -1:
        print("Just put in the folder name without using the full path, or any path separators.")
        exit(1)
    elif args.folder in Constants.LIST_OF_FOLDERS:
        print("ERROR: the folder you used is part of the list of main folders where the test cases belong.")
        exit(1)

    dict1 = outputParser(fullPathFile1)
    dict2 = outputParser(fullPathFile2)

    targetFolder = os.path.join(Constants.baseTestFolderPath, args.folder)

    if len(dict1) != len(dict2):
        print("Warning: the dictionaries aren't of the same length!")

    print("Length of dict1: " + str(len(dict1)))
    diffDict = {}

    for key in dict1:

        # TODO: add an option to distinguish between diff passes...
        # or even diff answers?
        if dict1.get(key).outcome != dict2.get(key).outcome:
            diffDict[key] = dict1.get(key)

    print("Difference found:")
    print(diffDict)

    print("Keys of diffs")
    for key in diffDict:
        print(key)

        print("Guess at folder:")
        print(diffDict[key].getOrigFolderOfTestcase())

        # TODO: handle filename collisions!
        shutil.copyfile(
            os.path.join(Constants.baseTestFolderPath, diffDict[key].getOrigFolderOfTestcase(), diffDict[key].filename),
            os.path.join(targetFolder, diffDict[key].filename))


if __name__ == '__main__':
    main()

# Example:
# python MoveStatusChangedTestcasesToFolder.py july22nd-1.txt july24th-2.txt -f TestPython