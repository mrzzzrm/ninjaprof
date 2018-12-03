import subprocess
import re


class NMFunctionSymbol:
    def __init__(self, name, code, size, file_and_line):
        self.name = name
        self.code = code
        self.size = size
        self.file_and_line = file_and_line


def run(path, demangle=False):
    if demangle:
        args = ["nm", "-C", path]
    else:
        args = ["nm", path]

    completed_process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")

    if completed_process.returncode != 0:
        print("Error running nm: {}".format(completed_process.stderr))
        return

    lines = completed_process.stdout.split("\n")
    function_symbols = []

    line_re = re.compile("([0-9a-z]+)?\s+([a-zA-Z])\s+(.*)")

    for line in lines:
        if len(line) == 0:
            continue

        match = line_re.match(line)
        if match is None:
            print("Skipping nm line '{}'".format(line))
            continue

        size = match.group(1)
        code = match.group(2)
        name = match.group(3)
        file_and_line = None

        if size is not None:
            size = int(size, 16)

        symbol = NMFunctionSymbol(name, code, size, file_and_line)
        function_symbols.append(symbol)

    return function_symbols


if __name__ == "__main__":
    function_symbols, unknown_symbols = run("/home/moritz/Coding/hyrise/cmake-build-ninja-clang-debug/src/lib/CMakeFiles/hyrise.dir/operators/join_nested_loop.cpp.o")

    print("Symbols: {} {}".format(len(function_symbols), len(unknown_symbols)))

