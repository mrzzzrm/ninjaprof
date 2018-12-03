import sys

import elf
from util import *


def main(args):
    object_file_path, = args

    object = elf.read_object(object_file_path, read_symbols=True)

    object.raw_symbols = sorted(object.raw_symbols, key=lambda object: object.name)

    for symbol in object.raw_symbols:
        print(symbol.name)


if __name__ == "__main__":
    main(sys.argv[1:])