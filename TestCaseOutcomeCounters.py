class TestCaseOutcomeCounters:
    numTestcases = 0

    numPasses = 0
    numFails = 0

    numBidFails = 0
    numLeadFails = 0
    numSecondFails = 0
    numThirdFails = 0
    numFourthFails = 0

    def incrementNumTestcases(self):
        self.numTestcases = self.numTestcases + 1

    def incrementNumPasses(self):
        self.numPasses = self.numPasses + 1

    def incrementNumFails(self):
        self.numFails = self.numFails + 1

    def incrementNumBidFails(self):
        self.numBidFails = self.numBidFails + 1

    def incrementNumLeadFails(self):
        self.numLeadFails = self.numLeadFails + 1

    def incrementNumSecondFails(self):
        self.numSecondFails = self.numSecondFails + 1

    def incrementNumThirdFails(self):
        self.numThirdFails = self.numThirdFails + 1

    def incrementNumFourthFails(self):
        self.numFourthFails = self.numFourthFails + 1

    def sanityCheckNumbersAddUp(self):
        if self.numTestcases != self.numPasses + self.numFails:
            print("WARNING: test cases don't add up 1")

        if self.numFails != self.numBidFails + self.numLeadFails + self.numSecondFails + self.numThirdFails + self.numFourthFails:
            print("WARNING: test cases don't add up 2")

    def incrementCounterBasedOnTestcaseObj(self, testCaseFileObj):

        self.incrementNumTestcases()

        if testCaseFileObj.outcome == 1:
            self.incrementNumPasses()
        else:
            self.incrementNumFails()

            if testCaseFileObj.failType == 'bid':
                self.incrementNumBidFails()

            elif testCaseFileObj.failType == 'lead':
                self.incrementNumLeadFails()

            elif testCaseFileObj.failType == 'second':
                self.incrementNumSecondFails()

            elif testCaseFileObj.failType == 'third':
                self.incrementNumThirdFails()

            elif testCaseFileObj.failType == 'fourth':
                self.incrementNumFourthFails()

    def printSummaryPercentages(self, counterType):

        print(counterType + ":  " + str(self.numPasses) + " / " + str(self.numTestcases) + " ( " + str(round((100 * self.numPasses)/self.numTestcases, 2)) + "% ) (" + str(self.numFails) + " fails)")
        print()

    def printCounterSums(self):
        print("numTestcases: " + str(self.numTestcases))
        print("numPasses: " + str(self.numPasses))
        print("numFails: " + str(self.numFails))
        print("numBidFails: " + str(self.numBidFails))
        print("numLeadFails: " + str(self.numLeadFails))
        print("numSecondFails: " + str(self.numSecondFails))
        print("numThirdFails: " + str(self.numThirdFails))
        print("numFourthFails: " + str(self.numFourthFails))
        print()
        print()
