#!/usr/bin/env python
"""Converts CHDK badpixel.bin to dcraw deadpixels.txt"""

import struct
import sys

assert(len(sys.argv) == 3)

infspec = sys.argv[1]
outfspec = sys.argv[2]

with open(infspec, 'rb') as f:
    with open(outfspec, 'w') as o:
        while True:
            d = f.read(2)
            if not d:
                break
            if len(d) != 2:
                raise RuntimeError(len(d))
            xval = struct.unpack_from('<H', d)[0]
            x = xval & 0x1fff #X (column) location with bad pixels
            xcount = (xval >> 13) + 1 #number of bad pixel records at this X
            d = f.read(2 * xcount)
            if len(d) != (2 * xcount):
                raise RuntimeError('{0} {1}'.format(xcount, len(d)))
            yvals = struct.unpack_from('<{0}H'.format(xcount), d)
            for yval in yvals:
                y = yval & 0x1fff
                ycount = (yval >> 13) + 1 #run of bad pixel records in y (row)
                for j in range(ycount):
                    o.write('{0:4d} {1:4d} 0\n'.format(x, y + j))
