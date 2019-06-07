# MIT License
#
# Copyright (c) 2019 Konstantinos Lountzis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import csv
import json


def main(args):
    if args.ifile is None:
        exit()

    delimiter = args.delimiter
    if args.delimiter is None:
        delimiter = ','

    settings = {}
    if args.mfile:
        with open(args.mfile, 'r') as m_file:
            settings = json.load(m_file)

    header = True

    data = []
    keys = []
    index = 0

    with open(args.ifile, 'r') as i_file:
        csv_reader = csv.reader(i_file, delimiter=delimiter)
        for row in csv_reader:
            if header:
                header = False
                keys = row
                continue

            json_object = {}
            for i in range(0, len(keys)):
                key = keys[i]
                value = row[i].strip()

                command = settings.get(key)
                if command is not None:
                    ignore = command.get("ignore")
                    if ignore:
                        continue
                    rename = command.get("rename")
                    if rename is not None:
                        key = rename
                    change = command.get("change")
                    if change is not None:
                        value = eval(change, {'value': value, 'index': index})
                json_object[key] = value
            data.append(json_object)
            index += 1

    if args.ofile:
        with open(args.ofile, 'w') as o_file:
            json.dump(data, o_file, indent=4)
            o_file.write('\n')
    else:
        print(json.dumps(data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV to JSON Files Converter.", epilog="Copyright (c) 2019 Konstantinos Lountzis")
    parser.add_argument("-i", "--ifile", required=True, type=str, help="CSV File")
    parser.add_argument("-m", "--mfile", required=False, type=str, help="JSON File")
    parser.add_argument("-o", "--ofile", required=False, type=str, help="JSON File")
    parser.add_argument("-d", "--delimiter", help="Default Delimiter is ','")
    args = parser.parse_args()
    main(args)
