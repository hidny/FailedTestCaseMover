import subprocess
import os

# TODO: number param for how far back

# TODO: --card for num cards last test case has to have.

from standardTestCaseCrawler import makeFileObjectFromFile

baseTestFolderPath = "/Users/Michael/GitHub/TestCaseAndReplayData/testcases"
folder = "Michael2022-3"

curTestFolder = baseTestFolderPath + "/" + folder

files = [f for f in os.listdir(curTestFolder) if os.path.isfile(os.path.join(curTestFolder, f))]

files.sort()

print(files)
print(files[-1])

subprocess.call([r"c:/Program Files (x86)/Notepad++/notepad++.exe", os.path.join(curTestFolder, files[-1])])


# TODO: --card for num cards.
# Example of this workign for num 5
#TODO: num cards between 2 and 13
for file in reversed(files):
    if len(makeFileObjectFromFile(curTestFolder, file).cardsInHand.strip().split(" ")) == 5:
        subprocess.call([r"c:/Program Files (x86)/Notepad++/notepad++.exe", os.path.join(curTestFolder, file)])
        break

#TODO: have option for prev bid.
# make TestCaseFileObj detect when there's no play history and have a flag that says it's a bid...