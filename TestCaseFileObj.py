class TestCaseFileObj:

    def __init__(self, filename, playerName, cardsInHand, folder='', outcome='', failType=''):
        self.filename = filename
        self.playerName = playerName
        self.cardsInHand = cardsInHand
        self.folder = folder
        self.outcome = outcome
        self.failType = failType

    def sameTestCaseDiffFolder(self, otherTestcase):
        return self.filename == otherTestcase.filename \
               and self.playerName == otherTestcase.filename \
               and self.cardsInHand == otherTestcase.cardsInHand

    def getKey(self):
        return self.filename + self.playerName

    def getFolder(self):
        if self.folder != '':
            self.folder
        else:
            print("Warrning: calling getFolder when folder is unknown")
            self.folder


print("Hello world")
