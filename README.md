# c2j

Just a utility python script I made to painlessly convert csv files to json ones. 

It provides the ability to customize the delimiter of the input csv file, as well as change the resulting json,  by renaming, ignoring, and/or transforming (by explicitly adding code) the value of the existing csv columns (See [example](/example)).

Two variables are exposed for the transformation: ```value``` , that represents the value of the column for the specific row and ```index```, that is the index of the row.

## Usage

Just download the python script and run it like this:

```
python3 c2j.py [-h] [-i IFILE] [-m MFILE] [-o OFILE] [-d DELIMITER]
```

## License
[MIT License](LICENSE)
