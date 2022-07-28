from os import listdir
from os.path import isfile, join

# TODO: put in config:
from TestCaseFileObj import TestCaseFileObj

LIST_OF_FOLDERS = \
    ("MichaelDebugMadeUp", "Michael", "Michael2021", "Michael2021-2", "doubleMellowTests", "Michael2022-3")
baseTestFolderPath = "/Users/Michael/GitHub/TestCaseAndReplayData/testcases"


# TODO: this is actually really slow...
# maybe save the mapping to a file and only call it if the file is missing entries?

def getAllStandardTestCasesAndFolders():
    dictTestcases = {}

    for folder in LIST_OF_FOLDERS:
        folderPath = baseTestFolderPath + "/" + folder
        files = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]

        for filename in files:

            tmpFileObj = makeFileObjectFromFile(folderPath, filename)

            if tmpFileObj.getKey() in dictTestcases:
                print("Warning: duplicate test case: " + tmpFileObj.getKey())
                print("Removing prev test case from list")

            dictTestcases[tmpFileObj.getKey()] = tmpFileObj
            print(tmpFileObj.getKey() + "---" + dictTestcases[tmpFileObj.getKey()].folder)

    return dictTestcases


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


if __name__ == '__main__':
    getAllStandardTestCasesAndFolders()