#!/usr/bin/env python

"""Rename images by focal length and f/ number"""

import glob
import os
import os.path
import subprocess

for f in sorted(list(glob.glob('*.CR2'))):
    exiv2_process = subprocess.Popen(
        ["exiv2", "-PEkt", "-g", "Exif.Photo.FocalLength", "-g", "Exif.Photo.FNumber", f], stdout=subprocess.PIPE)
    lines = exiv2_process.communicate()[0].splitlines()
    focal = float(lines[1].split()[-2])
    fno = float(lines[0].split()[-1][1:])
    os.rename(f, '{0:03.0f}_{1:04.1f}.CR2'.format(focal, fno))

