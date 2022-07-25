# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from os import listdir
from os.path import isfile, join

from TestCaseFileObj import TestCaseFileObj
from TestOutputParser import outputParser


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


#TODO: go thru list of test folders and catalog it all in a file seperate from main.
#folderName = '''C:\Users\Michael\GitHub\TestCaseAndReplayData\testcases\tmp'''
folderName = "/Users/Michael/GitHub/TestCaseAndReplayData/testcases/tmp"

onlyfiles = [f for f in listdir(folderName) if isfile(join(folderName, f))]

# Want files names with player names...
# + maybe the cards served just in case.


#TODO: be able to process input from git diff Testcase...
#TODO: be able to make a git diff call and make a file out of it

#I guess I just have to rm the + at the start?
#TODO: put this in a helper file

fileDict = {}

listOfFileDesc = []

for f in onlyfiles:
    print(str(f))

    filename = f
    nameOfPlayer = ''
    cards = ''

    file1 = open(join(folderName, f), 'r')
    count = 0

    line = ''
    previousLine = ''

    while True:
        count += 1

        # Get next line from file
        line = file1.readline()

        if(line.startswith("Your name: ")):
            nameOfPlayer = line.split(" ")[2].strip()
        elif(previousLine.startswith("Cards in hand:")):
            cards = line.strip()


        previousLine = line
        # if line is empty
        # end of file is reached
        if not line:
            break

        print("Line{}: {}".format(count, line.strip()))

    file1.close()

    print()
    folder = folderName.split("/")[-1]
    print("Folder: " + folder)
    print("Filename: " + filename)
    print("Name of player: " + nameOfPlayer)
    print("Cards: " + cards)


    print("----")
    tmpFileObj = TestCaseFileObj(filename, nameOfPlayer, cards, folder)
    print("Key: " + tmpFileObj.getKey())

    fileDict[tmpFileObj.getKey()] = tmpFileObj

print(listOfFileDesc)

print("Try something different:")

outputParser("animal.txt")
