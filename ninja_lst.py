import sys

import ninja
from util import *


def main(args):
    build_dir_path, = args

    build_dir = ninja.read_dir(build_dir_path, read_symbols=False)

    build_dir.objects = sorted(build_dir.objects.items(), key=lambda item: item[1].build_time, reverse=True)

    for name, object in build_dir.objects:
        print("{}: {} {}s".format(object.short_name, sizeof_fmt(object.file_size), object.build_time))


if __name__ == "__main__":
    main(sys.argv[1:])