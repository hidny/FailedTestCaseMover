import re

# TODO: put in config:
LIST_OF_FOLDERS = \
    ("MichaelDebugMadeUp", "Michael", "Michael2021", "Michael2021-2", "doubleMellowTests", "Michael2022-3")


class TestCaseFileObj:

    def __init__(self, filename, playerName, cardsInHand, folder='', outcome='', failType=''):
        self.filename = filename
        self.playerName = playerName
        self.cardsInHand = cardsInHand
        self.folder = folder
        self.outcome = outcome
        self.failType = failType

    def sameTestCaseDiffFolder(self, otherTestcase):
        return self.fgetFolderilename == otherTestcase.filename \
               and self.playerName == otherTestcase.filename \
               and self.cardsInHand == otherTestcase.cardsInHand

    def getKey(self):
        return self.filename + "," + self.playerName

    def getOrigFolderOfTestcase(self):

        cur_str = ""
        for m in self.filename:
            if m.isdigit():
                cur_str = cur_str + m
        #print("Find numbers from string:", cur_str)

        num = -1
        if len(cur_str) > 0:
            num = int(cur_str)

        #print("num: " + str(num))

        # TODO: 6000 should just be a constant (it's the line to go to debug cases)
        if num >= 6000:
            return "MichaelDebugMadeUp"

        elif self.playerName in LIST_OF_FOLDERS:
            return self.playerName

        else:
            return "MichaelDebugMadeUp"
