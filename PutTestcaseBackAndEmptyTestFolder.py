import argparse

import Constants
import shutil
import os

from TestcaseParsers import makeFileObjectFromFile


def main():
    parser = argparse.ArgumentParser(
        description='Move testcase from a test folder back to the main folders where they belong.')

    parser.add_argument("folderName", help="Folder name of test folder")
    parser.add_argument("-k", "--keep", help="Keep the test cases in the test folder", action="store_true")

    args = parser.parse_args()

    folder = args.folderName

    if folder.find('/') != -1 or folder.find('\\') != -1:
        print("Just put in the folder name without using the full path, or any path separators.")
        exit(1)

    # TODO: make this input:
    folderPath = os.path.join(Constants.baseTestFolderPath, args.folderName)

    if not os.path.exists(folderPath):
        print("ERROR: the folder does not exist.\nFull path searched:\n" + folderPath)
        exit(1)
    elif args.folderName in Constants.LIST_OF_FOLDERS:
        print("ERROR: the folder you used is part of the list of main folders where the test cases belong.")
        exit(1)

    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

    for filename in files:
        tmpFileObj = makeFileObjectFromFile(folderPath, filename)

        shutil.copyfile(
            os.path.join(folderPath, filename),
            os.path.join(Constants.baseTestFolderPath, tmpFileObj.getOrigFolderOfTestcase(), filename)
        )

        if not args.keep:
            os.remove(os.path.join(folderPath, filename))


if __name__ == '__main__':
    main()
