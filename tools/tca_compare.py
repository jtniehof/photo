#!/usr/bin/env python

import glob
import re

import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy


fnames = glob.glob('*.tca')
fits = {} #fits by filename
fls = {} #filenames by focal length
for fn in fnames:
    with open(fn, 'r') as f:
        lens, fl, fit = f.readlines()
    fl = fl.strip()
    fit = fit.strip()
    if not fl in fls:
        fls[fl] = [fn]
    else:
        fls[fl].append(fn)
    thisfit = re.match(r"-r [.0]+:(?P<br>[-.0-9]+):(?P<cr>[-.0-9]+):(?P<vr>[-.0-9]+) -b [.0]+:(?P<bb>[-.0-9]+):(?P<cb>[-.0-9]+):(?P<vb>[-.0-9]+)", fit).groupdict()
    for k in thisfit:
        thisfit[k] = float(thisfit[k])
    fits[fn] = thisfit

means = dict((
    (fl,
     dict((
         ('{0}{1}'.format(param, color),
          numpy.mean([fits[fn]['{0}{1}'.format(param, color)]
                      for fn in fls[fl]]))
         for color in ('r', 'b') for param in ('b', 'c', 'v'))))
    for fl in fls))

x = numpy.arange(0, 1.9, 0.1)
figpar = plt.figure()
axpar = figpar.add_subplot(111)
axpar.yaxis.set_major_formatter(
    matplotlib.ticker.ScalarFormatter(useOffset=False))
for color in 'r', 'b':
    figmean = plt.figure()
    axmean = figmean.add_subplot(111)
    axmean.yaxis.set_major_formatter(
        matplotlib.ticker.ScalarFormatter(useOffset=False))
    for param in 'b', 'c', 'v':
        fl = sorted(list(fls.keys()), key=float)
        xp = numpy.array(fl).astype(numpy.float64)
        p = '{0}{1}'.format(param, color)
        yp = numpy.array([means[i][p] for i in fl])
        if param is 'v':
            yp -= 1.
        axpar.plot(xp, yp, label=p)
    for fl in sorted(list(fls), key=float):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.ScalarFormatter(useOffset=False))
        b = means[fl]['b{0}'.format(color)]
        c = means[fl]['c{0}'.format(color)]
        v = means[fl]['v{0}'.format(color)]
        ax.plot(x, b * x ** 2 + c * x + v, label='Mean')
        axmean.plot(x, b * x **2 + c * x + v, label=fl)
        for fn in fls[fl]:
            b = fits[fn]['b{0}'.format(color)]
            v = fits[fn]['v{0}'.format(color)]
            ax.plot(x, b * x ** 2 + c * x + v, label=fn)
        ax.legend(loc='best')
        fig.suptitle('{0} {1}'.format(fl, color))
        fig.savefig('{0}_{1}.png'.format(fl, color))
    axmean.legend(loc='best')
    figmean.suptitle('{0}'.format(color))
    figmean.savefig('means_{0}.png'.format(color))
figpar.suptitle('Parameters')
axpar.set_xlabel('Focal length')
axpar.legend(loc='best')
figpar.savefig('parameters.png')
    
for fl in sorted(list(means.keys()), key=float):
    print("""            <tca model="poly3" focal="{0}" br="{1}" vr="{2}" bb="{3}" vb="{4}" />""".format(fl, means[fl]["br"], means[fl]["vr"], means[fl]["bb"], means[fl]["vb"]))
