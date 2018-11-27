import sys

def main(args):
    outputs = []

    groups = {
        "expression": 0,
        "logical_query_plan": 0,
        "operators": 0
    }

    total_duration = 0

    for line in open(args[0], 'r').readlines()[1:]:
        start, finish, _, output, _ = line.split('\t')

        if not output.startswith("src/lib"):
            continue

        duration = (int(finish) - int(start)) / 1000.0

        outputs.append((output, duration))
        total_duration += duration

    outputs = sorted(outputs, key=lambda output: output[1], reverse=True)

    for output in outputs:
        print(output)

    print("Compilation Units: {}".format(len(outputs)))
    print("Duration: {}".format(total_duration))


if __name__ == '__main__':
    main(sys.argv[1:])