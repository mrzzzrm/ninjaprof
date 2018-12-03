import os
import subprocess

import nm
import elf
from util import *

class BuildObject:
    def __init__(self, path):
        self.path = path
        self.build_time = 0
        self.file_size = 0

    def print(self):
        print("{}: {}s {}".format(self.path, self.build_time, sizeof_fmt(self.file_size)))


class BuildDir:
    def __init__(self, path):
        self.path = path
        self.objects = {}
        self.build_time = 0
        self.file_size = 0


def recompact(path):
    subprocess.run(["ninja", "-t", "recompact"], cwd=path)


def read_dir(build_dir_path, read_symbols=False, filter=None):
    recompact(build_dir_path)

    ninja_log_path = os.path.join(build_dir_path, ".ninja_log")

    build_dir = BuildDir(build_dir_path)
    build_time_total = 0
    file_size_total = 0

    for line in open(ninja_log_path, 'r').readlines()[1:]:
        start, finish, _, output, _ = line.split('\t')

        if output.endswith(".o") and (filter is None or output.startswith(filter)):
            build_object = elf.read_object(os.path.join(build_dir_path, output), read_symbols=read_symbols)
            build_object.build_time = (int(finish) - int(start)) / 1000.0

            build_dir.objects[output] = build_object

            build_time_total += build_object.build_time
            file_size_total += build_object.file_size

    build_dir.build_time = build_time_total
    build_dir.file_size = file_size_total

    return build_dir
