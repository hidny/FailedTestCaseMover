import os

import Constants
from UselessTestCaseCrawler import makeFileObjectFromFile


# TODO: number param for how far back

def appendLabelToFile(filname):
    with open(filname, 'a') as fd:
        fd.write(f'\n# (TODO: please test)')


# TODO: --card for num cards last test case has to have.


curTestFolder = os.path.join(Constants.baseTestFolderPath, Constants.curTestFolderBeingAddedTo)

files = [f for f in os.listdir(curTestFolder) if os.path.isfile(os.path.join(curTestFolder, f))]

files.sort()

print(files[-1])

appendLabelToFile(os.path.join(curTestFolder, files[-1]))

# TODO: --card for num cards.
# Example of this working for num 5
# TODO: num cards between 2 and 13

for file in reversed(files):
    if len(makeFileObjectFromFile(curTestFolder, file).cardsInHand.strip().split(" ")) == 7:
        appendLabelToFile(os.path.join(curTestFolder, file))
        break
