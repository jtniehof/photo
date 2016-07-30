#!/usr/bin/env python

"""Sort vignetting images by focal distance"""

import glob
import os
import os.path
import subprocess

for f in sorted(list(glob.glob('*.CR2'))):
    exiv2_process = subprocess.Popen(
        ["exiv2", "-PEkt", "-g", "Exif.CanonFi.FocusDistanceUpper", "-g", "Exif.CanonFi.FocusDistanceLower", f], stdout=subprocess.PIPE)
    lines = exiv2_process.communicate()[0].splitlines()
    upper = float(lines[0].split()[-2])
    lower = float(lines[1].split()[-2])
    dist = (upper + lower) / 2.
    if dist > 2.:
        subdir = 'vignetting'
    else:
        subdir = 'vignetting_{0:.2f}'.format(dist)
    if not os.path.isdir(subdir):
        os.mkdir(subdir)
    os.rename(f, os.path.join(subdir, f))

