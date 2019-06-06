import argparse
import json
import csv

def main(args):
    if args.input is None:
        exit()

    if args.output is None:
        exit()

    delimiter = args.delimiter
    if args.delimiter is None:
        delimiter = ','

    map_file = {}
    if args.map:
        with open(args.map, 'r') as f:
            map_file = json.load(f)

    data = []
    column_names = []
    is_header = True
    index = 0

    with open(args.input, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)
        for row in csv_reader:
            if is_header:
                is_header = False
                column_names = row
                continue

            data_object = {}
            for i in range(0, len(column_names)):
                column_name = column_names[i]
                column_value = row[i].strip()

                column_settings = map_file.get(column_name)
                if column_settings is not None:
                    is_ignored = column_settings.get("ignored")
                    if is_ignored:
                        continue
                    new_column_name = column_settings.get("new_name")
                    if new_column_name is not None:
                        column_name = new_column_name
                    transformation = column_settings.get("transformation")
                    if transformation is not None:
                        column_value = eval(transformation, {'value': column_value, 'index': index})
                data_object[column_name] = column_value
            data.append(data_object)
            index += 1

    with open(args.output, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        json_file.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input")
    parser.add_argument("-o", "--output", type=str, help="Output")
    parser.add_argument("-d", "--delimiter", type=str, help="Delimiter")
    parser.add_argument("-m", "--map", type=str, help="Map")
    args = parser.parse_args()
    main(args)