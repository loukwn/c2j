import argparse
import json
import csv


def main(args):
    if args.input is None:
        exit()

    delimiter = args.delimiter
    if args.delimiter is None:
        delimiter = ','

    map_file = {}
    if args.map:
        with open(args.map, 'r') as f:
            map_file = json.load(f)

    header = True

    data = []
    keys = []
    index = 0

    with open(args.input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            if header:
                header = False
                keys = row
                continue

            json_object = {}
            for i in range(0, len(keys)):
                key = keys[i]
                value = row[i].strip()

                settings = map_file.get(key)
                if settings is not None:
                    ignore = settings.get("ignore")
                    if ignore:
                        continue
                    rename = settings.get("rename")
                    if rename is not None:
                        key = rename
                    change = settings.get("change")
                    if change is not None:
                        value = eval(change, {'value': value, 'index': index})
                json_object[key] = value
            data.append(json_object)
            index += 1

    if args.output:
        with open(args.output, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            json_file.write('\n')
    else:
        print(json.dumps(data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input")
    parser.add_argument("-o", "--output", type=str, help="Output")
    parser.add_argument("-d", "--delimiter", type=str, help="Delimiter")
    parser.add_argument("-m", "--map", type=str, help="Map")
    args = parser.parse_args()
    main(args)
