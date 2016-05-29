# filestats
Find the (n) smallest or the (n) biggest file(s) in a directory, recursive or not, get the MD5 hash of the files, exclude files smaller than a specific size

filestats.py: file statistics.

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       -r/--recursive: recursive search
  -m, --md5             -m/--md5: get md5 hash
  -b BIGGER, --bigger BIGGER
                        -b/--bigger: add only files bigger than <bigger> bytes
  -d, --desc            -d/--desc: descending order
  -p PATH, --path PATH  -p/--path: path to search
  -n NUMBER, --number NUMBER
                        -n/--number: show top <number> files, "0" to print all
