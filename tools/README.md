# tools

## pgm.py

Python module for reading pgm files (simplest output from dcraw)

## badpixels.py

Convert a CHDK badpixel.bin file to a deadpixels.txt suitable for input to dcraw. Run as `badpixels.py badpixel.bin deadpixels.txt`

## finddead.py

Identifies dead (identically zero) pixels. Run on the pgm output from dcraw (rquires `pgm.py`). `finddead.py input.pgm deadpixels.txt`

Convert the raw to pgm with `dcraw -v -t 0 -4 -o 0 -M -D foo.DNG`

Combine multiple bad pixel lists with `cat deadpixels1 deadpixels2 | sort -k 1g -k 2g | uniq > allbad`

## tca_compare.py
Plots transverse chromatic aberration values across focal length and multiple images at one focal length; prints the mean values for each focal length. Run after Torsten's `calibrate.py` in the directory with the `.tca` files. 