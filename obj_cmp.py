import sys

import elf


def main(args):
    obj_path_a, obj_path_b = args

    obj_a = elf.read_object(obj_path_a, read_symbols=True)
    obj_b = elf.read_object(obj_path_b, read_symbols=True)

    symbols_a = {symbol.name for symbol in obj_a.raw_symbols}
    symbols_b = {symbol.name for symbol in obj_b.raw_symbols}

    symbols_only_in_a = sorted(symbols_a - symbols_b)
    symbols_only_in_b = sorted(symbols_b - symbols_a)
    symbols_in_both = sorted(symbols_a & symbols_b)

    print("{} symbols only in first file; {} symbols only in second file; {} in both".format(len(symbols_only_in_a), len(symbols_only_in_b), len(symbols_in_both)))

    print("--- Symbols only in first ---")
    for symbol in symbols_only_in_a:
        print(symbol)

    print("--- Symbols only in second ---")
    for symbol in symbols_only_in_b:
        print(symbol)


if __name__ == "__main__":
    main(sys.argv[1:])
