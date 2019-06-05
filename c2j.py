import getopt
import sys
import json
import csv

# defaults
delimiter = ','
input_file = ''
output_file = ''
column_mapping = {}


def main(argv):
    # parse command line args
    parse_args(argv)

    data_to_save = []
    column_names = []
    is_column_name_row = True
    index = 0

    # parse csv and save to JSON object
    with open(input_file) as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=delimiter)
        for row in csv_reader:

            # get column names
            if is_column_name_row:
                is_column_name_row = False
                column_names = row
                continue

            data_obj = {}
            for i in range(0, len(column_names)):
                column_name = column_names[i]
                column_value = row[i].strip()

                column_settings = column_mapping.get(column_name)
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

                data_obj[column_name] = column_value

            data_to_save.append(data_obj)
            index += 1

    # save data to json
    with open(output_file, 'w') as json_file:
        json.dump(data_to_save, json_file, indent=4)


def parse_args(argv):
    global input_file, output_file, delimiter, column_mapping

    try:
        opts, args = getopt.getopt(argv, "hi:o:d:m:", ["ifile=", "ofile=", "delimiter=", "column_map="])
    except getopt.GetoptError:
        show_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-d", "--delimiter"):
            delimiter = arg
        elif opt in ("-m", "--column_map"):
            if arg:
                with open(arg, 'r') as f:
                    column_mapping = json.load(f)


def show_usage():
    print("Usage: \n"+
        "python c2j.py -i <csv_file> -o <json_file> [-d <delimiter>] [-m <file_with_column_mapping_logic] \n "+
        "\n" +
        "Options:\n" +
        "\t-h                    Show this screen\n" +
        "\t-i --ifile            Set the input csv file\n" +
        "\t-o --ofile            Set the output json file\n" +
        "\t-d --delimiter        Set the csv delimiter (default ',')\n" +
        "\t-m --column_map       Set the file that contains the column mapping logic\n\n")


if __name__ == "__main__":
    argv = sys.argv[1:]
    if len(argv) < 4:
        show_usage()
        sys.exit(1)
    main(sys.argv[1:])
