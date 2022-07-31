import Constants
import shutil
import os
from TestcaseParsers import makeFileObjectFromFile


def main():
    # TODO: make this input:
    folderPath = os.path.join(Constants.baseTestFolderPath, "TestPython")

    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath, f))]

    for filename in files:
        tmpFileObj = makeFileObjectFromFile(folderPath, filename)

        shutil.copyfile(
            os.path.join(folderPath, filename),
            os.path.join(Constants.baseTestFolderPath, tmpFileObj.getOrigFolderOfTestcase(), filename)
        )

        os.remove(os.path.join(folderPath, filename))


if __name__ == '__main__':
    main()
