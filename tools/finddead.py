#!/usr/bin/env python
"""Find dead pixels (exactly zero) from a pgm (from RAW) and write badpixels.txt for dcraw input"""

#convert the raw with
#dcraw -v -t 0 -4 -o 0 -M -D foo.DNG

import sys

import numpy

import pgm

def main():
    data = pgm.read_pgm(sys.argv[1])
    rows, columns = numpy.nonzero(data == 0)
    idx = numpy.argsort(rows)
    rows = rows[idx]
    columns = columns[idx]
    idx = numpy.argsort(columns, kind='mergesort') #stable
    rows = rows[idx]
    columns = columns[idx]
    with open(sys.argv[2], 'w') as f:
        for i in range(len(rows)):
            #numpy is (row column) not (column row)
            f.write('{0:4d} {1:4d} 0\n'.format(columns[i], rows[i]))
    

if __name__ == "__main__":
    main()
