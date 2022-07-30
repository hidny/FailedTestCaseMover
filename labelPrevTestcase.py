import os
from standardTestCaseCrawler import makeFileObjectFromFile


# TODO: number param for how far back

def appendLabelToFile(filname):
    with open(filname, 'a') as fd:
        fd.write(f'\n# (TODO: please test)')


# TODO: --card for num cards last test case has to have.


# TODO: copy/paste code
baseTestFolderPath = "/Users/Michael/GitHub/TestCaseAndReplayData/testcases"
folder = "Michael2022-3"

curTestFolder = os.path.join(baseTestFolderPath, folder)

files = [f for f in os.listdir(curTestFolder) if os.path.isfile(os.path.join(curTestFolder, f))]

files.sort()

#print(files)
print(files[-1])
# End TODO copy/paste code

appendLabelToFile(os.path.join(curTestFolder, files[-1]))

# TODO: --card for num cards.
# Example of this workign for num 5
# TODO: num cards between 2 and 13

for file in reversed(files):
    if len(makeFileObjectFromFile(curTestFolder, file).cardsInHand.strip().split(" ")) == 7:
        appendLabelToFile(os.path.join(curTestFolder, file))
        break
