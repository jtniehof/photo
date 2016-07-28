#!/usr/bin/env/python

"""Run gnuplot files  (e.g. from calibrate.py vignetting)
from current directory and make pngs"""

import glob
import subprocess


for fname in glob.glob('*.gp'):
    with open(fname, 'r') as f:
        inlines = f.readlines()
    outlines = ['set terminal png size 1024,768\n']
    outlines.append("set output '{0}.png'\n".format(fname[:-3]))
    outlines.extend((i for i in inlines if not i.startswith('pause')))
    p = subprocess.Popen('gnuplot', stdin=subprocess.PIPE)
    p.communicate(''.join(outlines))
