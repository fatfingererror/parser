from __future__ import print_function

import sys
from pprint import pprint as pp

from parser import WeekFormatter, Parser, CsvReader


def main():
    """main entrypoint, read the 3 filenames and print the result of 
    the parsing in console"""
    fnames = sys.argv[1:4]
    for name in fnames:
        reader = CsvReader(name)
        formatter = WeekFormatter()
        parser = Parser(reader, formatter)
        out = parser.parse()
        print(name)
        pp(out)
        print()

main()
