import argparse

import Constants
from GetPrevTestcase import findRelevantFileBasedOnArgs


def appendLabelToFile(filname, labelToUse):
    with open(filname, 'a') as fd:
        fd.write(f'\n' + labelToUse)


def main():
    parser = argparse.ArgumentParser(description="Append label to previous testcase."
                                                 " Default label is \"" + Constants.DEFAULT_LABEL + "\"")

    listCardNumAvailable = []
    for i in range(2, Constants.MAX_CARDS_IN_A_HAND + 1):
        listCardNumAvailable.append(i)

    parser.add_argument("-n", "--num", default=1, help="Label the nth last test case", type=int)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--card", help="Filter for non-bid test cases with a specific number of cards", type=int,
                       choices=listCardNumAvailable)
    group.add_argument("-b", "--bid", help="Filter for bid test cases", action="store_true")

    parser.add_argument("-l", "--label", default=Constants.DEFAULT_LABEL, help="Label to add. Put it in quotes and begin with a \"#\"."
                                              "\nExample: \"" + Constants.DEFAULT_LABEL + "\"")

    args = parser.parse_args()
    labelToUse = args.label

    fileToLabel = findRelevantFileBasedOnArgs(args)
    appendLabelToFile(fileToLabel, labelToUse)


if __name__ == '__main__':
    main()
