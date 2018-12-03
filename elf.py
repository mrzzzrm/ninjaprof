import os
import subprocess

import nm
from util import *


class ELFObject:
    def __init__(self, path):
        self.short_name = os.path.split(path)[-1]
        self.path = path
        self.build_time = 0
        self.file_size = 0
        self.raw_symbols = []

    def print(self):
        print("{}: {}s {} {} raw symbols".format(self.path, self.build_time, sizeof_fmt(self.file_size), len(self.raw_symbols)))


def demangle(name):
    completed_process = subprocess.run(["/home/moritz/.cargo/bin/cppfilt", name], encoding="utf-8", stdout=subprocess.PIPE)
    return completed_process.stdout[:-1]


def read_object(path, read_symbols=False, demangle_mode="None", cluster_symbols=False):
    elf_object = ELFObject(path)
    elf_object.file_size = os.path.getsize(path)

    if read_symbols:
        elf_object.raw_symbols = nm.run(path, demangle=demangle_mode == "nm_demangle")

    if demangle_mode == "cpp_demangle":
        for raw_symbol in elf_object.raw_symbols:
            raw_symbol.name = demangle(raw_symbol.name)

    return elf_object


if __name__ == "__main__":
    obj = read_object("/home/moritz/Coding/hyrise/cmake-build-ninja-clang-debug/src/lib/CMakeFiles/hyrise.dir/operators/join_nested_loop.cpp.o", read_symbols=True, cluster_symbols=True)