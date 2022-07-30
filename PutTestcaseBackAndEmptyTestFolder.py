

from TestOutputParser import outputParser
import shutil
import os

# TODO: maybe the path before the folder name could be a config.
from standardTestCaseCrawler import makeFileObjectFromFile

baseTestFolderPath = "/Users/Michael/GitHub/TestCaseAndReplayData/testcases"

def main():
    # TODO: make this input:
    folderPath = baseTestFolderPath + "/" + "TestPython"

    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

    for filename in files:

        tmpFileObj = makeFileObjectFromFile(folderPath, filename)

        shutil.copyfile(
            folderPath + "/" + filename,
            baseTestFolderPath + "/" + tmpFileObj.getOrigFolderOfTestcase() + "/" + filename
        )

        os.remove(folderPath + "/" + filename)




if __name__ == '__main__':
    main()
