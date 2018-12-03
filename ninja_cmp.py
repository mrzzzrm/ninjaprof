import sys

import ninja


def main(args):
    assert(len(args) == 3)

    sort_by_name, build_dir_path_a, build_dir_path_b = args

    sort_by_idx = {"build_time": 0, "file_size": 1, "symbol_count": 2}[sort_by_name]

    build_a = ninja.read_dir(build_dir_path_a, read_symbols=False, filter="src/lib/")
    build_b = ninja.read_dir(build_dir_path_b, read_symbols=False, filter="src/lib/")

    differences = {}

    for name, build_object_a in build_a.objects.items():
        if name not in build_b.objects:
            print("{} not found in second build dir".format(name))
            continue

        build_object_b = build_b.objects[name]

        differences[name] = []
        differences[name].append(build_object_b.build_time - build_object_a.build_time)
        differences[name].append(build_object_b.file_size - build_object_a.file_size)
        differences[name].append(len(build_object_b.raw_symbols) - len(build_object_a.raw_symbols))

    print()

    differences_sequential = [(name, difference) for name, difference in differences.items()]

    differences_sorted = sorted(differences_sequential, key=lambda difference: difference[1][sort_by_idx])

    for name, difference in differences_sorted:
        print(name, difference)

    #print()

    #for name, difference in differences_sorted[-10:]:
    #    print(name, difference)

    build_time_abs_diff = build_b.build_time - build_a.build_time
    build_time_rel_diff = (build_time_abs_diff / build_a.build_time) * 100
    file_size_abs_diff = build_b.file_size - build_a.file_size
    file_size_rel_diff = (file_size_abs_diff / build_a.file_size) * 100

    print()
    print("ObjectCount {} -> {}".format(len(build_a.objects), len(build_b.objects)))
    print("BuildTime {:.2f}s -> {:.2f}s ({:.2f}s {:.2f}%)".format(build_a.build_time, build_b.build_time, build_time_abs_diff, build_time_rel_diff))
    print("FileSize {} -> {} ({} {:.2f}%)".format(ninja.sizeof_fmt(build_a.file_size), ninja.sizeof_fmt(build_b.file_size), ninja.sizeof_fmt(file_size_abs_diff), file_size_rel_diff))


if __name__ == "__main__":
    main(sys.argv[1:])