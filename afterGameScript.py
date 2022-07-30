from os import listdir
from os.path import isfile, join

# TODO: put in config:
from TestCaseFileObj import TestCaseFileObj

# TODO:
# git diff 4e0a826761cb7d2bbaa8c50dae797383b886f0ec 3c332fcc7e33ad23db814a27d1074ab5d1700345 > C:\Users\Michael\Desktop\gitDiff.txt

#
# C:\Users\Michael\Desktop\gitDiff.txt
from TestOutputParser import sanityCheckNumbersAddUp


def goThruGitDiff(folderPath, filename):
    file = open(join(folderPath, filename), 'r')
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

        print(line)

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

    lastTestcase = TestCaseFileObj(filename, nameOfPlayer, cards, folder)

    testFileDict[lastTestcase.getKey()] = lastTestcase

    print("Line count: " + str(count))
    print("numTestcases: " + str(len(testFileDict)))

    return testFileDict


if __name__ == '__main__':
    goThruGitDiff("/Users/Michael/Desktop", "gitDiff.txt")
