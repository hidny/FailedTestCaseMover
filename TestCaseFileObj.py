

# TODO (optional): Add option to add details about when testcase is bid, lead, 2nd, 3rd, 4th even when it's not a fail
import Constants


class TestCaseFileObj:

    def __init__(self, filename, playerName, cardsInHand, isBid, hasTODOLabel, hasCustomLabel, folder='', outcome='', failType=''):
        self.filename = filename
        self.playerName = playerName
        self.cardsInHand = cardsInHand
        self.isBid = isBid
        self.hasTODOLabel = hasTODOLabel
        self.hasCustomLabel = hasCustomLabel
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
        # print("Find numbers from string:", cur_str)

        num = -1
        if len(cur_str) > 0:
            num = int(cur_str)

        # print("num: " + str(num))

        if num % Constants.ORD_MAG_END_OF_TESTCASES >= Constants.TESTCASE_NUMBER_WHERE_DEBUG_TESTS_START:
            return Constants.DEBUG_FOLDER_NAME

        elif self.playerName in Constants.LIST_OF_FOLDERS_WITH_TESTCASES:
            return self.playerName

        else:
            return Constants.DEBUG_FOLDER_NAME
