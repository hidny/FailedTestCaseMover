import Constants
from TestOutputParser import outputParser
import os
import shutil


def main():
    # TODO: make this input:
    dict1 = outputParser("/Users/Michael/Desktop/july24th-1.txt")

    dict2 = outputParser("/Users/Michael/Desktop/july24th-2.txt")

    targetFolder = os.path.join(Constants.baseTestFolderPath, "TestPython")

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
