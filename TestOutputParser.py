# tODO: make this a helper function
from TestCaseFileObj import TestCaseFileObj


# TODO: maybe add option to get fail counts or test case list.
# TODO: compare fail counts to other output files so we could fill in the table


# TODO: Combine with all other parsers in single util file?
from TestcaseParsers import outputParser

if __name__ == '__main__':
    outputParser("/Users/Michael/Desktop/july24th-1.txt")

'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--filename", help="Test case output filename",
                    type=str)

args = parser.parse_args()

if args.filename:
    print(args.filename)

    outputParser(args.filename)

'''
