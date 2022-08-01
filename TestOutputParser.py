import argparse

import Constants
from TestcaseParsers import outputParser
import os


def main():
    parser = argparse.ArgumentParser(description=
                                     "Go through test parser output and count fails.\n"
                                     "This is more of a sanity check.\n"
                                     "If it's not specified, input file will be assumed to be on desktop "
                                     "(i.e: " + Constants.DESKTOP_LOCATION + ").")

    parser.add_argument("filename", help="File name if on desktop, or full path")

    args = parser.parse_args()

    if args.filename.find("/") != -1:
        fullPath = args.filename
    else:
        fullPath = os.path.join(Constants.DESKTOP_LOCATION, args.filename)

    outputParser(fullPath)


if __name__ == '__main__':
    main()
